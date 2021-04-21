/*MongoDB Practice: 

1) Create a new Mongo Database
2) load 6 Documents into a Collection all at once
3) Show how to delete the 3rd and 5th documents
4) Display the remaining 4 documents. */

//TO CREATE A NEW MONGO DB

    // Install MongoDB from website
    // include it in my path in system env variables menu
    // run mongo from cmd to start mongo shell - mongod just pukes a bunch of data
    mongo
    // start a new db from shell
    use test 

//LOADING UP SEVERAL DOCUMENTS INTO A COLLECTION

    // make sure we have a collection to access, so we create...
    db.createCollection("myAwesomeCollection")
    // throw some data in there using insertMany... it's important these go in with square brackets
    db.myAwesomeCollection.insertMany([
        {
            "book_id": 1,
            "title": "The Ringworld Engineers",
            "author": "Larry Nivan"
        },

        {
            "book_id": 2,
            "title": "The Spirit Of St. Louis",
            "author": "Charles A. Lindbergh"
            
        },
        {
            "book_id": 3,
            "title" : "Aces & Eights",
            "author": "Loren D. Estleman"
            
        },
        {
            "book_id": 4,
            "title" : "Famous Men Who Never Lived",
            "author": "K Chess"
            
        },
        {
            "book_id": 5,
            "title" : "No Longer Human",
            "author": "Osamu Dazai"
            
        },
        {
            "book_id": 6,
            "title" : "The Science of Dreams",
            "author": "Edwin Diamond"
            
        }
    ])

//DELETING MULTIPLE ITEMS FROM A DATABASE

    // Technically I can delete multiple with individual deletions...
    db.myAwesomeCollection.remove({"book_id": 3})
    db.myAwesomeCollection.remove({"book_id": 5})
    // but I can do many too
    db.myAwesomeCollection.deleteMany(
        {
            "book_id": {$in: [3, 5]}
        }
    )

//DISPLAYING THE RESULT FROM THE DATABASE

    db.myAwesomeCollection.find().pretty()

    //result below:
/*
    {
        "_id" : ObjectId("6080b4fc0b994d74543d69d8"),
        "book_id" : 1,
        "title" : "The Ringworld Engineers",
        "author" : "Larry Nivan"
}
{
        "_id" : ObjectId("6080b4fc0b994d74543d69d9"),
        "book_id" : 2,
        "title" : "The Spirit Of St. Louis",
        "author" : "Charles A. Lindbergh"
}
{
        "_id" : ObjectId("6080b4fc0b994d74543d69db"),
        "book_id" : 4,
        "title" : "Famous Men Who Never Lived",
        "author" : "K Chess"
}
{
        "_id" : ObjectId("6080b4fc0b994d74543d69dd"),
        "book_id" : 6,
        "title" : "The Science of Dreams",
        "author" : "Edwin Diamond"
}
*/