from Entity.Util import EntityBase
_EntityBase = EntityBase.EntityBase

from Entity.Util import Enumerables
_RawTextType = Enumerables.RawTextType
_PlagiarismObfuscation = Enumerables.PlagiarismObfuscation
_PlagiarismType = Enumerables.PlagiarismType
_EnumYesNo = Enumerables.EnumYesNo

from Entity.RawDataBase import TextCollectionMeta
_TextCollectionMeta = TextCollectionMeta.TextCollectionMeta
from Entity.RawDataBase import RawText
_RawText = RawText.RawText
from Entity.RawDataBase import RawTextPair
_RawTextPair = RawTextPair.RawTextPair
from Entity.RawDataBase import Detection
_Detection = Detection.Detection
from Entity.RawDataBase import Pan
_PanFolderStructure = Pan.PanFolderStructure
_PanDetectionXmlStructure = Pan.PanDetectionXmlStructure
_PanDetectionXmlPlain = Pan.PanDetectionXmlPlain

from Entity.PreProcessing import RawTextExcerptLocation
_RawTextExcerptLocation = RawTextExcerptLocation.RawTextExcerptLocation
from Entity.PreProcessing.Bag import BagOfTexts
_BagOfTexts = BagOfTexts.BagOfTexts