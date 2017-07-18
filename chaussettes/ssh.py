import re
import collections
import logging
import subprocess

module_logger = logging.getLogger('chaussettes.ssh')

class Config:

   _rx = re.compile(r'^ \s* (\w+) (?: \s*=\s* | \s+) (.*) $', re.X)

   def __init__(self, filename=None, fileobj=None):
      assert (filename is not None) != (fileobj is not None),\
             "Either filename or fileobj shall be given but not both"
      if not fileobj:
         fileobj = open(filename)
      options = []
      self.hosts = []
      seen_hosts = set()
      for line in fileobj:
         m = self._rx.search(line)
         if m is not None:
            options.append(m.group(1,2))
      host_indices = [i for i,o in enumerate(options) if o[0] == 'Host']
      host_indices.append(len(options))
      for k in range(len(host_indices)-1):
         i,j = host_indices[k:k+2]
         host = options[i][1]
         if host in seen_hosts:
            continue
         h = {'host':host}
         for l in range(i+1, j):
            keyword, arguments = options[l]
            h[keyword.lower()] = arguments
         self.hosts.append(Host(**h))
         seen_hosts.add(host)

class Host:

   def __init__(self, host, **kwds):
      self.host = host
      self.__dict__.update(kwds)

   def __getattr__(self):
      return None

   def __eq__(self, other):
      return self.__dict__ == other.__dict__
