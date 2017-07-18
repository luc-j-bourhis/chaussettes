from chaussettes import ssh

from io import StringIO

def test_single_simple():
  config = ssh.SshConfig(fileobj=StringIO("""\
  Host somewhere
  Hostname a.b.c.d
  User paul
  """))
  assert config.hosts == [
    ssh.Host(Host='somewhere',
             Hostname='a.b.c.d',
             User='paul')
  ]

def test_multiple_simple():
  config = ssh.SshConfig(fileobj=StringIO("""\

  Host somewhere
  Hostname a.b.c.d
  User paul

  #

  Host somewhere.else
  Hostname e.f
  Host somewhere.else.altogether
  Hostname g.h.i
  User peter
  """))
  assert config.hosts == [
    ssh.Host('somewhere',
         Hostname='a.b.c.d',
         User='paul'),
    ssh.Host('somewhere.else',
         Hostname='e.f'),
    ssh.Host('somewhere.else.altogether',
         Hostname='g.h.i',
         User='peter')
  ]

def test_single_more_complex():
  config = ssh.SshConfig(fileobj=StringIO("""\
  Host=somewhere
    Hostname = my.address.com
      Compression= no
    RequestTTY =auto
    ForwardX11 no
    Ciphers chacha20-poly1305@openssh.com
  """))
  assert config.hosts == [
    ssh.Host('somewhere',
         Hostname='my.address.com',
         Compression='no',
         RequestTTY='auto',
         ForwardX11='no',
         Ciphers='chacha20-poly1305@openssh.com')
    ]

