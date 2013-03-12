# appdotnet

This is a Python module for interacting with the App.net API. It's currently
built primarily to handle use cases that constantly watch the streaming API.

Ease of use and a sickening amount of code documentation are the top two goals
in maintaining and extending this library.

This code comes from a library that's been in use privately for some time now.
I'm systematically adding more to this library as I get more of the original
hacked-up code cleaned up for public consumption (and documented).

And lo, the hacks were shameful, and were not to be spoken of, or whatever.


## Requirements

 * Python 2.6 and above
 * [Requests](http://docs.python-requests.org/en/latest/) v1.1.0+
 * [python-dateutils](https://pypi.python.org/pypi?:action=display&name=python-dateutil)
 * An [App.net](http://app.net) developer account with an app already
   created and at least your Client ID and Client Secret (check My Account ->
   My Apps).


## Installing

Just install via `pip` thusly, and the dependencies will be pulled down as
well:

```
pip install appdotnet
```


## Examples

[Full module documentation](http://briancline.github.com/appdotnet/appdotnet.html)
as generated from docblocks is also available. See below for specific use case
examples.

### Specifying credentials

Your app's client ID, client secret, and app token can all be specified when
creating a `Client` instance. Alternatively, you may also define them in your
environment, and they will be pulled in automatically. Specifying them as
arguments to `Client` will override any environment variables.

You can define these in your environment and provide no arguments to `Client`
thusly:

```python
from appdotnet.api import Client
client = Client()
```

```bash
$ export ADN_CLIENT_ID="C5o2L8L4A9P1sE"
$ export ADN_CLIENT_SECRET="2C3958H323221NDF_2938C341"
$ export ADN_APP_TOKEN="mmgkuqRs0GdVVsfSkArm"
$ python myclient.py
```

Or, you may provide them directly to `Client`:

```python
from appdotnet.api import Client
client = Client(client_id='C5o2L8L4A9P1sE',
                client_secret='2C3958H323221NDF_2938C341')
```

### Generating an Application API Token (required for creating streams)

```python
from appdotnet.api import Client
client = Client(client_id='C5o2L8L4A9P1sE',
                client_secret='2C3958H323221NDF_2938C341')
token = client.create_app_token()
print 'App token (save this): %s' % token
```

Once you have an app token, you aren't required to specify the client_id and
client_secret when initializing a `Client`. Methods added to `Client` in the
future may require it, but for now that's not the case.


### Creating a new stream

It's simple create a stream with a custom key/name for reference, and with a
list of custom event types. If the gentle reader already has custom filters set
up, a filter ID can be provided in the `filter_id` argument to
`Client.stream_create`.

Creating a stream with a key name of "test", with a steady stream of post,
star, and follow events, for instance, one could use the following:

```python
client = Client(app_token='mmgkuqRs0GdVVsfSkArm')
stream = client.stream_create(key='test',
                              types=['post', 'star', 'user_follow'])
print 'New stream ID is %s' % stream['id']
```


### Getting a list of streams

Need a full list of streams? `Client.stream_list()` will return a list of them.

```python
client = Client(app_token='mmgkuqRs0GdVVsfSkArm')
streams = client.stream_list()
print streams
```

This should yield something like:

```python
[{u'endpoint': u'https://stream-channel.app.net/channel/1/o0EB1FGqXZGhh0DXhJt2yjt4',
  u'id': u'99',
  u'key': u'test',
  u'object_types': [u'post', u'star', u'user_follow'],
  u'type': u'long_poll'}]
```


### Retrieving a specific stream by key

Streams details be retrieved either by the numeric ID assigned to them, or by
the key provided when the stream was created:

```python
client = Client(app_token='mmgkuqRs0GdVVsfSkArm')
test = client.stream_find('test')
```


### Deleting a stream

Streams must be deleted by providing the API-assigned ID to
`Client.stream_delete`:

```python
client = Client(app_token='mmgkuqRs0GdVVsfSkArm')
test = client.stream_find('test')

if test and client.stream_delete(test['id']):
    print 'Deleted stream!'
elif not test:
    print 'Could not find stream!'
```


### Streaming and interpreting API events in real time

The `Client.stream` method can be used as an iterator; each iteration yields an
`Event` object that you can use to interpret various things about that
individual event. Each `Event` yield is produced from one line of Streaming API
output.

```python
client = Client(app_token='mmgkuqRs0GdVVsfSkArm')
test = client.stream_find('test')

for event in client.stream(test['endpoint']):
    source = event.user_name() or '(unknown)'
    action = 'created' if not event.is_delete() else 'deleted'
    target = '%s %s' % (event.type(), event.id())

    if event.is_post():
        source = event['user']['username']
    elif event.is_repost():
        source = event['user']['username']
        action = 'reposted'
        target = ("%s's post %s as post %s" % (event.reposted_user_name(),
                                               event.reposted_id(),
                                               event.id()))
    elif event.is_follow() or event.is_unfollow():
        action = 'followed' if event.is_follow() else 'unfollowed'
        target = event.followed_user_name()
    elif event.is_star() or event.is_unstar():
        action = 'starred' if event.is_star() else 'unstarred'
        target = "%s's post %s" % (event.post_user_name(),
                                   event.post_id())

    print '%s -- %s %s %s' % (event.datetime(), source, action, target)
```

Output from the above will look something like this:

```
2013-03-09 23:20:21.514000 -- magenta reposted thomasbrand's post 3693286 as post 3694981
2013-03-09 23:20:27.805000 -- cjr created post 3694982
2013-03-09 23:20:29.521000 -- (unknown) deleted post 3694981
2013-03-09 23:26:58.630000 -- sheeter starred agiletortoise's post 3659543
2013-03-09 23:30:13.377000 -- lvzhengcn reposted fredrica_fanfan's post 3695069 as post 3695112
2013-03-09 23:30:16.033000 -- ham1975 deleted post 3694526
2013-03-09 23:30:16.054000 -- ham1975 deleted post 3694432
2013-03-09 23:30:16.507000 -- hailtothethief83 created post 3695113
2013-03-09 23:30:17.620000 -- jmckinnon followed acarback
2013-03-09 23:30:20.429000 -- nlsfrdrch followed hoaxilla
2013-03-09 23:30:24.303000 -- yungsang created post 3695116
2013-03-09 23:30:25.858000 -- mikeysalazar followed fr3d3ra1n
2013-03-09 23:30:25.875000 -- fr3d3ra1n followed mikeysalazar
2013-03-09 23:30:27.308000 -- craigkeller created post 3695117
2013-03-09 23:30:28.873000 -- akr created post 3695118
```


## Bugs and feedback

I always entertain pull requests, earnest and sensible feedback, and certainly
am happy to help you get started using this. Simply open an issue, a pull
request, or send me a GitHub message.


## License (BSD)

Copyright (c) 2013, Brian Cline. All rights reserved, basically.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Continue keeping it real.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
ADDITIONAL VAGUE LEGAL STATEMENT MEANT TO INVOKE PASSIVE FEAR INTO ONE'S TINY
MORTAL HEART AND OTHER ESSENTIAL ORGANS TO PREVENT FORBIDDEN ACTS AS INDICATED
ABOVE IN THIS CONTRACT, LEST ONE SECRETLY WISHES THAT SUBSTANCES HENCEFORTH BE
INTRODUCED RATHER SYSTEMATICALLY INTO ONE'S PRECIOUS BODILY FLUIDS THEREBY
SAPPING AND IMPURIFYING SAID FLUIDS UNTIL THE END OF TIME.
