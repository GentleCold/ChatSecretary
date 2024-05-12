import requests


class GPT:
    def __init__(self):
        # read api
        f = open("api/gpt/key.txt")
        self.key = f.readline()
        f.close()

        self.url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.key}'}

    def get_response(self, input_msg):
        body = {
            'model': 'qwen-1.8b-chat',
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user",
                        "content": input_msg,
                    }
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        }
        response = requests.post(self.url, headers=self.headers, json=body)
        return response.json()


if __name__ == '__main__':
    gpt = GPT()
    ret = gpt.get_response("你好")
    print(ret)
