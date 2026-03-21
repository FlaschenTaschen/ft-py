"""Tests for the ft-debugger CLI tool."""

import pytest

from flaschen_taschen.cli.ft_debugger import main


class TestDebuggerCLI:
    """Test debugger CLI."""

    def test_help(self, capsys):
        """Test --help flag."""
        result = main(["--help"])
        assert result == 0
        captured = capsys.readouterr()
        assert "FlaschenTaschen Debugger" in captured.out or "Standard Options" in captured.out

    def test_edges_mode(self, capsys):
        """Test edges mode with short timeout."""
        result = main(["-m", "edges", "-t", "1"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Done" in captured.out
        assert "frames" in captured.out

    def test_fill_mode(self, capsys):
        """Test fill mode with short timeout."""
        result = main(["-m", "fill", "-t", "1"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Done" in captured.out

    def test_default_mode(self, capsys):
        """Test default mode is edges."""
        result = main(["-t", "1"])
        assert result == 0
        captured = capsys.readouterr()
        assert "Done" in captured.out

    def test_geometry_parsing(self, capsys):
        """Test custom geometry."""
        result = main(["-g", "32x24", "-t", "1"])
        assert result == 0

    def test_with_delay(self, capsys):
        """Test with frame delay."""
        result = main(["-d", "10", "-t", "1"])
        assert result == 0

    def test_invalid_geometry(self):
        """Test invalid geometry format."""
        result = main(["-g", "invalid", "-t", "1"])
        assert result == 1
