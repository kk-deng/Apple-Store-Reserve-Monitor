import json
import os
from pathlib import Path


# Create a local proxy cache folder
saved_path = os.path.join(
    os.path.dirname(
        # os.path.dirname(
        os.path.dirname(__file__)
        # )
    ), "resources")
# print(saved_path)
Path(saved_path).mkdir(parents=True, exist_ok=True)


class ResponseVault:

    def __init__(self, spider_name: str = 'test'):
        self.spider_name = spider_name

    def write_data(self, data, extra_info: str = 'N/A', extra_name: str = '') -> bool:
        """Save data to a file (json for dicts, txt for strings)"""

        abs_filename = self.get_abs_filename(extra_name=extra_name)

        try:
            if isinstance(data, dict):
                # If it's dict, save to .json
                abs_filename += '.json'

                data['metadata'] = extra_info

                with open(abs_filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

            elif isinstance(data, str):
                # If it's str, save to .txt
                abs_filename += '.txt'

                data = data + f'\n{extra_info}'

                with open(abs_filename, 'w', encoding='utf-8') as f:
                    f.write(data)
            else:
                raise ValueError("Input data must be a dict or a string")
        except Exception as e:
            raise Exception(f'Failed to save data: {e}')

        return abs_filename

    def load_data(self, extra_name: str = ''):
        abs_filename = self.get_abs_filename(extra_name=extra_name)

        with open(abs_filename, 'r', encoding='utf-8') as f:
            return f.read()

    def load_json(self, extra_name: str = '') -> dict:
        abs_filename = self.get_abs_filename(extra_name=extra_name)
        abs_filename += '.json'

        with open(abs_filename) as json_file:
            return json.load(json_file)

    def get_abs_filename(self, extra_name: str = '') -> str:
        filename = self.spider_name + extra_name
        abs_filename = os.path.join(saved_path, filename)

        return abs_filename


if __name__ == "__main__":
    content = {
        "file": "abc",
        "test": [1, 2, 3, 4, 5]
    }
    saver = ResponseVault()
    saver.write_data(content)
    content = {
        "file": "abc",
        "test": [1, 2, 3, 4, 5, 6, 7]
    }
    saver.write_data(content, extra_name='_123')
