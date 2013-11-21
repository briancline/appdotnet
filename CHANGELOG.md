# appdotnet Changes

## 0.1.3 (2013-11-20)

 * Several changes to fix code smell warnings raised by landscape.io.
 * Fix bug where Event.followed_user_id was not using its default value.

## 0.1.2 (2013-03-11)

 * Changed mutable arg defaults in all instances with None, defaulting in the
   body instead, due to Python's issue with mutable defaults.
 * Add missing arg details in the _params docblock.
 * Add :returns: directives in docblocks.
 * Add Sphinx configuration.

## 0.1.1 (2013-03-10)

 * Fix an index error in `Client.stream_list()`.
 * Fix an attribute error in `Event.reposted_user_name()` and
   `Event.reposted_user_id()`.

## 0.1.0 (2013-03-09)

 * Implemented basic client object, streaming iterator, Event object, and
   convenience methods for the streaming API.
 * Initial publish to pypi.python.org.

