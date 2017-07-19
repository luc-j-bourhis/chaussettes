""" Interface to SSH """

import re
import collections
import logging
import subprocess


module_logger = logging.getLogger('chaussettes.ssh')
""" Logger for this module """

class Config:
   """ SSH configuration, i.e. the info stored in ~/.ssh/config


   """

   _rx = re.compile(r'^ \s* (\w+) (?: \s*=\s* | \s+) (.*) $', re.X)

   def __init__(self, filename=None, fileobj=None):
      """ Read the configuration from the given file or filename """
      assert (filename is not None) != (fileobj is not None),\
             "Either filename or fileobj shall be given but not both"

      self.hosts = []
      """ The list of hosts: each item is an instance of class `Host` """

      if not fileobj:
         fileobj = open(filename)
      options = []
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
   """ Info about a SSH host

   To each valid keyword as per ssh-config(5) corresponds an instance attribute,
   in lowercase, so as to support the case insentivity of ssh-config keywords.
   For a non-specified keyword, the value of the attribute is None.
   """

   PORT = 1080
   """ The port used for the SOCKS proxy on localhost """

   def __init__(self, host, **kwds):
      self.host = host
      self.__dict__.update(kwds)
      self.ssh = None

   def __getattr__(self):
      return None

   def __eq__(self, other):
      """ Two instances are equal if they have the same keywords
      set with the same values """
      return self.__dict__ == other.__dict__

   def __str__(self):
      """ The string representation is simply the Host """
      return self.host

   def connect(self):
      """ Establish a dynamic forward with self.host """
      module_logger.info("Connect {}".format(self.host))
      self.ssh = subprocess.Popen(
         ('ssh', '-N', '-D', str(self.PORT), self.hostname or self.host))

   def disconnect(self):
      """ Bring down the dynamic forward if it is established;
      otherwise do nothing """
      if self.ssh is not None:
         module_logger.info("Disconnect {}".format(self.hostname or self.host))
         self.ssh.terminate()
         self.ssh.wait()
