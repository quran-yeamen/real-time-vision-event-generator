import yaml

from src.pipeline import VisionEventPipeline


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def main() -> None:
    config = load_config("configs/pipeline_config.yaml")
    pipeline = VisionEventPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()