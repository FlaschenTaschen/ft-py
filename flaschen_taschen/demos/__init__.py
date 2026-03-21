"""FlaschenTaschen interactive demos framework.

Provides the base Demo class that all demos inherit from, along with
utility functions for demo discovery and execution.
"""

import sys
import time
from abc import ABC, abstractmethod
from typing import Optional

from flaschen_taschen.client.canvas import Canvas
from flaschen_taschen.client.config import Config
from flaschen_taschen.standard_options import StandardOptions


class Demo(ABC):
    """Base class for all FlaschenTaschen interactive demos.

    Lifecycle:
    1. __init__(std_opts) - Initialize with StandardOptions
    2. setup() - Set up canvas and resources
    3. Main loop:
       - update() - Compute frame logic
       - draw() - Render to canvas
       - send() - Transmit frame
    4. cleanup() - Release resources

    Subclasses implement update() and draw() at minimum.
    """

    def __init__(self, std_opts: StandardOptions):
        """Initialize demo with standard options.

        Args:
            std_opts: StandardOptions with parsed CLI arguments
        """
        self.std_opts = std_opts
        self.canvas: Optional[Canvas] = None
        self._frame_count = 0
        self._start_time: Optional[float] = None
        self._last_frame_time: Optional[float] = None

    def setup(self) -> None:
        """Initialize canvas and demo-specific resources.

        Override in subclass if custom initialization needed.
        """
        # Create config from standard options
        config = Config(
            host=self.std_opts.hostname,
            width=self.std_opts.width,
            height=self.std_opts.height,
            x_offset=self.std_opts.xoff,
            y_offset=self.std_opts.yoff,
            frame_delay_ms=self.std_opts.delay,
            layer=self.std_opts.layer,
        )
        self.canvas = Canvas(config, auto_send=False)
        self._start_time = time.time()
        self._last_frame_time = self._start_time

    @abstractmethod
    def update(self) -> None:
        """Update demo state for the current frame.

        Called once per frame. Update any animations, timers, or state.
        Must be implemented by subclass.
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """Render current frame to canvas.

        Called after update(). Use self.canvas to draw.
        Must be implemented by subclass.
        """
        pass

    def send(self) -> None:
        """Transmit frame to display.

        Can be overridden for custom frame sending logic.
        """
        if self.canvas:
            self.canvas.send()
            self._frame_count += 1

    def cleanup(self) -> None:
        """Release resources.

        Override if custom cleanup needed (e.g., close files).
        """
        if self.canvas and self.canvas.connection:
            self.canvas.connection.close()

    def run(self) -> None:
        """Main demo execution loop.

        Runs for specified timeout, calling update/draw/send each frame.
        Handles frame rate control based on standard delay option.
        """
        try:
            self.setup()
            assert self.canvas is not None

            timeout = self.std_opts.timeout
            start_time = time.time()

            while True:
                # Check timeout
                elapsed = time.time() - start_time
                if elapsed >= timeout:
                    break

                # Update and draw frame
                self.update()
                self.draw()
                self.send()

                # Frame rate control
                if self.std_opts.delay > 0:
                    frame_time = self.std_opts.delay / 1000.0  # Convert ms to seconds
                    elapsed_frame = time.time() - (self._last_frame_time or time.time())
                    sleep_time = max(0, frame_time - elapsed_frame)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    self._last_frame_time = time.time()

        finally:
            self.cleanup()

    @property
    def fps(self) -> float:
        """Get average frames per second."""
        if self._start_time is None or self._frame_count == 0:
            return 0.0
        elapsed = time.time() - self._start_time
        return self._frame_count / elapsed if elapsed > 0 else 0.0


def run_demo(demo_class, args: Optional[list] = None) -> None:
    """Helper to run a demo from command line.

    Args:
        demo_class: Demo subclass to instantiate
        args: Command-line arguments (defaults to sys.argv[1:])
    """
    if args is None:
        args = sys.argv[1:]

    std_opts = StandardOptions(args)
    demo = demo_class(std_opts)
    demo.run()
