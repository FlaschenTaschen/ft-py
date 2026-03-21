"""Tests for video generator."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flaschen_taschen.generators.video import VideoGenerator
from flaschen_taschen.client.color import Color


class TestVideoGenerator:
    """Test VideoGenerator class."""

    @pytest.fixture
    def mock_canvas(self):
        """Create a mock canvas."""
        canvas = Mock()
        canvas.width = 45
        canvas.height = 35
        canvas.clear = Mock()
        canvas.set_pixel = Mock()
        canvas.send = Mock()
        return canvas

    def test_init(self, mock_canvas):
        """Test VideoGenerator initialization."""
        gen = VideoGenerator(mock_canvas, 'test.mp4')
        assert gen.video_path == 'test.mp4'
        assert gen.canvas == mock_canvas
        assert gen.frame_rate == 30
        assert gen.frame_delay == 1.0 / 30

    def test_init_custom_frame_rate(self, mock_canvas):
        """Test initialization with custom frame rate."""
        gen = VideoGenerator(mock_canvas, 'test.mp4', frame_rate=24)
        assert gen.frame_rate == 24
        assert gen.frame_delay == 1.0 / 24

    @patch('subprocess.Popen')
    def test_extract_frames_ffmpeg_not_found(self, mock_popen, mock_canvas):
        """Test ffmpeg not found error."""
        mock_popen.side_effect = FileNotFoundError()

        gen = VideoGenerator(mock_canvas, 'test.mp4')

        with pytest.raises(RuntimeError, match='ffmpeg not found'):
            list(gen._extract_frames_ffmpeg())

    @patch('subprocess.Popen')
    @patch('flaschen_taschen.generators.video.Image')
    def test_extract_frames_ffmpeg_success(self, mock_pil, mock_popen, mock_canvas):
        """Test successful frame extraction."""
        mock_image = Mock()
        mock_pil.frombytes.return_value = mock_image

        # Mock ffmpeg process with byte-by-byte reading
        mock_proc = Mock()

        # Create a generator that yields frame data
        frame_data = b'P6\n45 35\n255\n' + b'\x00' * (45 * 35 * 3) + b''
        frame_idx = [0]

        def read_bytes(size):
            idx = frame_idx[0]
            frame_idx[0] += size
            if idx >= len(frame_data):
                return b''
            return frame_data[idx:idx + size]

        mock_proc.stdout.read = read_bytes
        mock_proc.terminate.return_value = None
        mock_proc.wait.return_value = None
        mock_popen.return_value = mock_proc

        gen = VideoGenerator(mock_canvas, 'test.mp4')

        # Should get at least one frame
        frames = list(gen._extract_frames_ffmpeg())
        assert len(frames) >= 1

    @patch('subprocess.Popen')
    @patch('time.sleep')
    @patch('flaschen_taschen.generators.video.Image')
    def test_render_video(self, mock_pil, mock_sleep, mock_popen, mock_canvas):
        """Test video rendering."""
        mock_image = Mock()
        mock_image.width = 45
        mock_image.height = 35
        mock_image.resize.return_value = mock_image
        mock_image.load.return_value = {(x, y): (255, 0, 0) for x in range(45) for y in range(35)}
        mock_pil.frombytes.return_value = mock_image
        mock_pil.LANCZOS = 1  # Mock constant

        # Mock ffmpeg process with byte-by-byte reading
        mock_proc = Mock()
        frame_data = b'P6\n45 35\n255\n' + b'\x00' * (45 * 35 * 3) + b''
        frame_idx = [0]

        def read_bytes(size):
            idx = frame_idx[0]
            frame_idx[0] += size
            if idx >= len(frame_data):
                return b''
            return frame_data[idx:idx + size]

        mock_proc.stdout.read = read_bytes
        mock_proc.terminate.return_value = None
        mock_proc.wait.return_value = None
        mock_popen.return_value = mock_proc

        gen = VideoGenerator(mock_canvas, 'test.mp4')
        gen.render(duration=0.1)

        assert mock_canvas.send.called

    def test_render_without_pillow(self, mock_canvas):
        """Test render raises without Pillow."""
        gen = VideoGenerator(mock_canvas, 'test.mp4')

        with patch.dict('sys.modules', {'PIL': None}):
            with patch('flaschen_taschen.generators.video.HAS_PILLOW', False):
                with pytest.raises(RuntimeError, match='Pillow not installed'):
                    gen.render()
