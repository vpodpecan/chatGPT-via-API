# Chat with ChatGPT via the OpenAI API


This litte script enables you to chat with a server which supports OpenAI API. It is especially suitable to use with ChatGPT-4. OpenAI Plus subscription costs 20$ per month and you have to sign up for waitlist. However, you can use ChatGPT-4 via API without waitlist if you put some money in your account. If the total number of tokens you exchange with ChatGPT-4 does not exceed those 20$ per month you can save some money (20$ will buy lots of tokens, like 1M+). In addition, you get easy python interface and the option to modify the context, save, load and continue chats.

The script can be used in python programs via the `ChatDialog` class or from the command line which gives you the live chat experience.


## Requirements

-  python 3.7+ and [openai python package v1.3+](https://pypi.org/project/openai/)
-  OpenAI API key or access to an [OpenChat](https://github.com/imoneoi/openchat) server


## Examples


From python:


```python
from chat_via_api import ChatDialog

# initialization and chat
gpt = ChatDialog(api_key='xxxxxxxxxxx',
                 organization='xxxxxxxxxxxx',  # this is optional
                 model='gpt-4-1106-preview',
                 role='You act as a helpful assistant')
print(gpt.ask('Tell me a joke'))

# saving and loading the object
gpt.save('gpt-test-1.pickle')
gpt1 = ChatDialog.load('gpt-test-1.pickle')
print(gpt1.ask('That joke was not funny. Tell me a better one.'))

# printing the complete dialog into a file
gpt1.print_context('gpt-test-1-chat.txt')
```


From command line:

### ChatGPT

```bash
python chat_via_api.py --api_key=xxxxxxxxxxx --organization=xxxxxxxxxxxx --model=gpt-4-1106-preview --role="You act as a data analyst specialized in text analysis"
```

### OpenChat

```bash
python chat_via_api.py --api_key=xxxxxxxxxxx --model=openchat_3.5 --base_url="http://localhost:18888/v1"
```

## License

MIT

## Contact

vid.podpecan@ijs.si

