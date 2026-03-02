"""Configuration module for Mike's Journey Home."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any
import tomli
import tomli_w

CONFIG_DIR = Path(Path.home() / ".mikes_game")
CONFIG_FILE_PATH = CONFIG_DIR / "config.toml"



@dataclass
class AppConfig:
    """App configuration settings."""

    mistral_api_key: str
    screen_width: int = 800
    screen_height: int = 600
    difficulty: str = "medium"
    starting_city: str = "Tokyo"
    fps: int = 60
    draw_collision_boxes: bool = False
    show_fps: bool = True
    log_ai_responses: bool = False
    debug: bool = False

    @classmethod
    def load(cls, config_path: str = CONFIG_FILE_PATH) -> "AppConfig":
        """Load configuration from TOML file or create default."""
        try:
            config_ = cls._load_config_file(config_path)
        except FileNotFoundError:
            config_ = cls._create_default_config(config_path)
        
        return cls(
            mistral_api_key=config_.get("mistral", {}).get("api_key", ""),
            screen_width=config_.get("game", {}).get("screen_width", 800),
            screen_height=config_.get("game", {}).get("screen_height", 600),
            difficulty=config_.get("game", {}).get("difficulty", "medium"),
            starting_city=config_.get("game", {}).get("starting_city", "Tokyo"),
            fps=config_.get("game", {}).get("fps", 60),
            draw_collision_boxes=config_.get("debug", {}).get("draw_collision_boxes", False),
            show_fps=config_.get("debug", {}).get("show_fps", True),
            log_ai_responses=config_.get("debug", {}).get("log_ai_responses", False)
        )

    @classmethod
    def _load_config_file(cls, config_path: str = CONFIG_FILE_PATH) -> Dict[str, Any]:
        """Load TOML config file."""
        with open(config_path, "rb") as f:
            return tomli.load(f)

    @classmethod
    def _create_default_config(cls, config_path: str = CONFIG_FILE_PATH) -> Dict[str, Any]:
        """Create default config file."""
        default_config = {
            "mistral": {"api_key": ""},
            "game": {
                "difficulty": "medium",
                "starting_city": "Tokyo",
                "screen_width": 1280,
                "screen_height": 720,
                "fps": 60
            },
            "debug": {
                "draw_collision_boxes": False,
                "show_fps": True,
                "log_ai_responses": False
            }
        }
        
        # Ensure directory exists
        config_dir = Path(config_path).parent
        if config_dir:
            config_dir.mkdir(exist_ok=True, parents=True)
        
        # Write default config
        with open(config_path, "wb") as f:
            tomli_w.dump(default_config, f)
        
        return default_config

    def save(self, config_path: str = "config.toml") -> None:
        """Save current configuration to file."""
        config_ = {
            "mistral": {"api_key": self.mistral_api_key},
            "game": {
                "difficulty": self.difficulty,
                "starting_city": self.starting_city,
                "screen_width": self.screen_width,
                "screen_height": self.screen_height,
                "fps": self.fps
            },
            "debug": {
                "draw_collision_boxes": self.draw_collision_boxes,
                "show_fps": self.show_fps,
                "log_ai_responses": self.log_ai_responses
            }
        }
        
        with open(config_path, "wb") as f:
            tomli_w.dump(config_, f)


if __name__ == "__main__":
    try:
        config = AppConfig.load()
        print("Configuration loaded successfully:")
        print(f"Mistral API key: {config.mistral_api_key}")
        print(f"Game difficulty: {config.difficulty}")
        print(f"Debug settings: {config.debug}")
    except Exception as error:
        print(f"Error loading config: {error}")