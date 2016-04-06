from bioLookupTables import BioLookupTables
from bioPeopleTables import BioPeopleTables
import logging

logger = logging.getLogger(__name__)

class EtlRun( object ):
	"""
		The EtlRun Classes job is to guarentee and force ordered execution of the 
		etl modules required for each etl process.
		There are 2 distinct modes this class will run in, 
			1: as a subquery select mode ( first run ), and
			2: in a list select mode ( second run ) 
		The select type is always in reference to how we get the data out of the 
		source database, the select type is determined by the emplids list, if the
		list is empty it is assumed that the mode is select by subquery, otherwise
		select by whats in the list.
		@sesSource - is the source database sqlalchemy session
		@sesTarget - is the target database sqlalchemy session
		@emplids - a list of emplids that appear missing in the target db people table

		returns: 
			exceptions
			logging
			"""
	def __init__( self, sesSource, sesTarget, emplids=[] ):
		self.sesSource = sesSource
		self.sesTarget = sesTarget
		self.missingEmplid = emplids
		
	
	def getMissingEmplid( self ):
		"""Return the emplids stored within the class attribute"""
		return self.missingEmplid


	def run( self ):
		"""
			The contract of what each process run will.
			Order Matters:


		"""
		# if first run... do this stuff, else skip.
		if not self.missingEmplid:
			logger.info("Processing Data for Lookup Tables:  BEGINNING")
			try:
				BioLookupTables( self.sesSource, self.sesTarget )
				logger.info("Lookup Tables data processing:  COMPLETED")
			except Exception as e:
				raise e

		logger.info("Processing Personnel Data:  BEGINNING")
		try:
			peopleRun = BioPeopleTables( self.sesSource, self.sesTarget, self.missingEmplid )
			peopleRun.runMe()
			logger.info("Personnel data processing:  COMPLETED")
		except Exception, e:
			raise e
