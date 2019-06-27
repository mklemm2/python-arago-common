import gssapi
from requests_gssapi import HTTPSPNEGOAuth
from gssapi.raw import acquire_cred_with_password, acquire_cred_from

class HTTPManagedSPNEGOAuth(HTTPSPNEGOAuth):
	def __init__(self, creds=None, principal=None, keytab=None, password=None, ccache=None, min_lifetime=300, *args, **kwargs):
		self.principal_name = gssapi.Name(principal, gssapi.NameType.kerberos_principal) if principal else None
		self.keytab_store = {'client_keytab': keytab}
		self.password = password.encode('utf-8')
		self.creds = creds
		self.ccache = ccache
		self.min_lifetime = min_lifetime
		if not self.creds:
			self.acquire_creds()
		super().__init__(creds=self.creds, *args, **kwargs)

	def acquire_creds(self):
		if self.principal_name and self.password:
			self.acquire_cred_generic(acquire_cred_with_password, name=self.principal_name, password=self.password, usage='initiate')
		elif self.principal_name and self.keytab_store['client_keytab']:
			self.acquire_cred_generic(acquire_cred_from, store=self.keytab_store, name=self.principal_name, usage='initiate')
		else:
			raise NotImplementedError("To acquire credentials, the principal and one of password or keytab must be given.")

	def store_creds(self):
		if self.ccache:
			store = {'ccache': self.ccache}
			self.creds.store(store, overwrite=True)

	def acquire_cred_generic(self, func, *args, **kwargs):
		raw_cred, mechs, lifetime = func(*args, **kwargs)
		self.creds = gssapi.Credentials(base=raw_cred)
		self.store_creds()

	def __call__(self, *args, **kwargs):
		try:
			lifetime = self.creds.lifetime
		except gssapi.raw.exceptions.ExpiredCredentialsError:
			lifetime = 0
		if lifetime < self.min_lifetime:
			self.acquire_creds()
		return super().__call__(*args, **kwargs)
