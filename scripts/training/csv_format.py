import pandas
import os
data = pandas.read_csv('../../input_audio/p_audio/processed_data.csv')

data['formatted'] = data['processed_path'] + '|' + data['text']

new_csv_path = os.path.join('../../input_audio', 'formatted.csv')
data['formatted'].to_csv('../../input_audio/formatted.csv', index = False, header = False)
