const button = document.querySelector("button")

button.addEventListener("click", () => {
    Notification.requestPermission().then(perm => {
        // alert(perm)
        if(perm === "granted"){
            new Notification("Example Notification", {
                
            }) //Allegedly web and phone compatible.
        }
    })
})

// TODO: Event listener for when automatic scan begins
// TODO: Event listener for when automatic scan ends

// Ideally should read from config.ini to see what settings user has configured
