# Readme

## What it is
Here I create a TCP chatroom using scokets and threading in python for unilateral messaging between client and server side instances.


## What I did
I refactored the server side to validate admin acess to make sure that correct routing for the kick and ban functions are present and not
vulnerable to client side manipulaiton. 

## How I did it
To do this I set a series of functions in place to one initialize the socket between server and client side, then allowing the request/response cycle to be validated at scale allowing multiple processes via broadcast traffic using the threading modules. Using broadcast as the designated traffic method for this chat room an end user can go in choose a nickname and begin chatting, if the request is validated as an admin then access control begins with validating the root user. The root user has the ability to kick, and ban chatters at anytime. 