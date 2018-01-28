#Config parameters
Logging = True
cacheTime = 1 #In hours
clearCacheTime = "23:00" # the time when the clear cache function will be called
webApiAddr = "http://httpbin.org"
#Entry points
activitiesEntryPoint = webApiAddr.join("/activities")
branchesEntryPoint = webApiAddr.join("/branches")
chaptersEntryPoint = webApiAddr.join("/chapters")
contactsEntryPoint = webApiAddr.join("/contacts")
usersEntryPoint = webApiAddr.join("/users")
#File Paths
membershipPath = "../resources/MembresiaIEEE.pdf"
chapterMembershipPath = "../resources/MembresiaIEEE.pdf"
#Default Messages
startReply = "Bienvenido al Bot de IEEE Computer Society TEC"
unrecognizedReply = "Comando invalido, por favor utilice el teclado especial."
closeReply = "Gracias por utilizar nuestro bot."