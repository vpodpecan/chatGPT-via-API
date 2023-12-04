import os
import sys
import pathlib
import logging
import pickle
import argparse

from openai import OpenAI


class ChatDialog:
    def __init__(self, 
                 api_key,
                 organization=None,
                 model='gpt-4-1106-preview', 
                 base_url='https://api.openai.com/v1',
                 role='You act as a helpful assistant'):
        self.base_url = base_url
        self.organization = organization
        self.api_key = api_key
        self.model = model
        self.role = role

        self.messages = []
        if self.role:
            self.messages.append({"role": "system", "content": self.role})
        self.client = self.create_client()

    def create_client(self):
        return OpenAI(api_key=self.api_key,
                      base_url=self.base_url,
                      organization=self.organization)
    
    @classmethod
    def load(klas, pickle_file):
        with open(pickle_file, 'rb') as fp:
            instance = pickle.load(fp)
        instance.client = instance.create_client()  # it was removed before dumping
        return instance

    def save(self, pickle_file):
        self.client = None  # this will avoid pickling _thread.RLock' object
        with open(pickle_file, 'wb') as fp:
            pickle.dump(self, fp)
        self.client = self.create_client()
    
    def ask(self, question):
        self.messages.append({"role": "user", "content": question})
        response = self.client.chat.completions.create(model=self.model,
                                                       messages=self.messages)
        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer

    def reset(self):
        self.messages = []
        if self.role:
            self.messages.append({"role": "system", "content": self.role})

    def print_context(self, filename=None):
        lines = []
        for i, message in enumerate(self.messages):
            if message['role'] == 'assistant':
                prefix = 'ANSWER'
            elif message['role'] == 'user':
                prefix = 'QUESTION'
            elif message['role'] == 'system':
                prefix = 'SYSTEM'
            else:
                prefix = '?'
            lines.append(f'{prefix}: {message["content"]}')
        if filename is not None:
            with open(filename, 'w') as fp:
                fp.write('\n'.join(lines))
        else:
            print('\n'.join(lines))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', required=True, help='Your API key')
    parser.add_argument('--organization', default=None, required=False, help='Organization ID')
    parser.add_argument('--model', required=False, default='gpt-4-1106-preview', help='Chat model to be used')
    parser.add_argument('--base_url', required=False, default='https://api.openai.com/v1', help='Link to the api URI')
    parser.add_argument('--role', required=False, default='You act as a helpful assistant', help='Initial instructions to the model')
    args = parser.parse_args()

    chat = ChatDialog(args.api_key,
                      organization=args.organization,
                      model=args.model,
                      base_url=args.base_url,
                      role=args.role)
    while True:
        question = input('Type a message: ')
        print(chat.ask(question))
        print('')
        