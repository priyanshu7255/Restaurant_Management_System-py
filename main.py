from  SRC.Authentication import manageprofile
from SRC.Domain import Orderprocessing
from SRC.Domain import Generatebills


manageprofile.AuthenticationMenu()
Orderprocessing.order()
Generatebills.bills()