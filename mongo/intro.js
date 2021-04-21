/*
It's easier to first write in a js script when doing Mongo db things
*/

db.createUser({
    user: 'maud',
    pwd: 'secret',
    customData: { startDate: new Date() },
    roles: [
        { role: 'clusterAdmin', db: 'admin' },
        { role: 'readAnyDatabase', db: 'admin' },
        'readWrite'
    ]   
})

//Basic use examples:
/*use mongoTest - switches to mongoTest but also creates
show dbs - shows all databases
db.getUsers() - shows all Users in current db 
db.dropUser('maud') - deletes a User in current db*/

//this creates a collection
/*db.createCollection('books')
show collections - literally shows your collections*/

//how to add to collection
db.books.insert({
    "name": "The Art of Tom Thomson",
    "publishedDate": new Date(),
    "authors": [
        {"name": "Unknown"}
    ]
})

//Drop everything: db.books.remove({})

//How to insert many//
db.books.insertMany([
    {
        "name": "Marijuana Potency",
        "publishedDate": new Date(),
        "authors": [
            {"name": "Michael Starks"}
        ]
    },
    {
        "name": "The Spirit Of St. Louis",
        "publishedDate": new Date(),
        "authors": [
            {"name": "Charles A. Lindbergh"}
        ]
    },
    {
        "name": "A book",
        "publishedDate": new Date(),
        "authors": [
            {"name": "An author"}
        ]
    }
])

//A pretty way to view our collection aka all our documents
db.books.find().pretty()

// cluttered version cuts the .pretty() part//

//A pretty way to find just one document in our collection
db.books.find( {name: "A book"} ).pretty()

//Can we update to Mark Z.D. for House of Leaves?

//wildcard * is considered bad practice

// How to query multiple things and show extra data with binary yes or no
db.books.find(
    {
        name: "House of Leaves"
    },
    {
        _id: 0,
        name: 1,
        publishedDate: 1, 
        authors: 1
    }
).pretty()

// How to query for a portion of a string
// oh no a really long book name
db.books.insert({
    "name": "This Is A Super Long Title About Very Long Title Things: The Sequel",
    "publishedDate": new Date(),
    "authors": [
        {"name": "Unknown"}
    ]
})

// time to whip out some regex...
// the i makes it case insensitive

db.books.findOne(
{ name: /.*the sequel.*/i },
{
    _id: 0,
    name: 1,
}
)

// how to remove documents
db.books.remove({name: "This Is A Super Long Title About Very Long Title Things: The Sequel", 1)
// the 1 deletes only 1, if you omit it it deletes everything //

// how to insert and then query more complex stuff
db.books.insert({
    "name": "Blink",
    "publishedDate": new Date(),
    "authors": [
        { "name": "Malcolm Gladwell", "active": "true" },
        { "name": "Ghost Writer", "active": "true" }
    ]
});


db.books.find(
    {
        name: "Blink"
    },
    {
        name: 1,
        publishedDate: 1,
        "authors.name": 1 // note this embedded nested value of showing authors active
    }
).pretty()

// the name nested in the authors looks for "name" attribute in the "authors" object
// need to have in quotes
// Can query inside things with their numeric values

// this returns how many match this query due to the length of array
db.books.find({name: "Blink"}).length()

// finds you just one entry and in a nice format
db.books.findOne({name: "Blink"})

//If you want to find a specific book so much, just search for an ID or do your best to have an explicit query

// How to check if a field exists - let's put in a new book
db.books.insert({
    "name": "Aces & Eights",
    "publishedDate": new Date(),
    "review" : 100,
    "authors": [
        { "name": "Loren D. Estleman" }
    ]
});

// This is handy for updating old files to a new formatting of the data
db.books.replace({ name: {$exists: true}}).pretty()

// $rename is how we could update a key
// update and replace are other updating methods
// note: you cannot rename a key that doesn't exist...
db.books.updateOne({ name: "Ace and Eights" }, { $set: {name: "Ace & Eights"} })