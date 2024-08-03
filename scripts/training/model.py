import json
import nemo.collections.tts as tts

config_path = '../../config/config.json'
with open(config_path, 'r') as f:
    config = json.load(f)

model = tts.models.Tacotron2Model.from_pretrained(model_name="Tacotron2-22050Hz")

model.setup_training_data(train_data_config=config['train_dataset'])
model.setup_validation_data(val_data_config=config['validation_dataset'])

model.train()