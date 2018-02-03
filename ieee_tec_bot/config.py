# Config parameters
Logging = True
cacheTime = 1  # In hours
clearCacheTime = "23:00"  # The time when the clear cache function will run
webApiAddr = "http://httpbin.org"
# Entry points
activitiesEntryPoint = "".join([webApiAddr, "/activities"])
branchesEntryPoint = "".join([webApiAddr, "/branches"])
chaptersEntryPoint = "".join([webApiAddr, "/chapters"])
contactsEntryPoint = "".join([webApiAddr, "/contacts"])
usersEntryPoint = "".join([webApiAddr, "/users"])
registerEntryPoint = "".join([webApiAddr, "/register"])
# File Paths
membershipPath = "../resources/MembresiaIEEE.pdf"
chapterMembershipPath = "../resources/MembresiaIEEE.pdf"
# Default Messages
startReply = "Bienvenido al Bot de IEEE Computer Society TEC"
unrecognizedReply = "Comando invalido, por favor utilice el teclado especial."
closeReply = "Gracias por utilizar nuestro bot."
