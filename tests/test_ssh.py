from chaussettes import ssh

from io import StringIO

def test_single_simple():
  config = ssh.Config(fileobj=StringIO("""\
  Host somewhere
  Hostname a.b.c.d
  User paul
  """))
  assert config.hosts == [
    ssh.Host(host='somewhere',
             hostname='a.b.c.d',
             user='paul')
  ]

def test_multiple_simple():
  config = ssh.Config(fileobj=StringIO("""\

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
         hostname='a.b.c.d',
         user='paul'),
    ssh.Host('somewhere.else',
         hostname='e.f'),
    ssh.Host('somewhere.else.altogether',
         hostname='g.h.i',
         user='peter')
  ]

def test_single_more_complex():
  config = ssh.Config(fileobj=StringIO("""\
  Host=somewhere
    Hostname = my.address.com
      Compression= no
    RequestTTY =auto
    ForwardX11 yes
    Ciphers chacha20-poly1305@openssh.com
  """))
  assert config.hosts == [
    ssh.Host('somewhere',
         hostname='my.address.com',
         compression=False,
         requesttty='auto',
         forwardx11=True,
         ciphers='chacha20-poly1305@openssh.com')
    ]
  assert not config.chaussettes_hosts

def test_chaussettes_option():
  config = ssh.Config(fileobj=StringIO("""\
  Host=somewhere
    #Chaussettes yes
    Hostname = my.address.com
      Compression= no
    RequestTTY =auto
    ForwardX11 no
    Ciphers chacha20-poly1305@openssh.com
  """))
  assert config.hosts == [
    ssh.Host('somewhere',
         chaussettes=True,
         hostname='my.address.com',
         compression=False,
         requesttty='auto',
         forwardx11=False,
         ciphers='chacha20-poly1305@openssh.com')
    ]
  assert config.chaussettes_hosts == config.hosts

def test_default_value():
  config = ssh.Config(fileobj=StringIO("Host=somewhere"))
  assert len(config.hosts) == 1
  h = config.hosts[0]
  assert h.forwardx11 is None
