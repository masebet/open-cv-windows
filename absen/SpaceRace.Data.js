var firebaseConfig = {
    apiKey: "AIzaSyDBsmD_FysCO73gesWHBN4MSqxnCdLYljg",
    authDomain: "getdata-real.firebaseapp.com",
    databaseURL: "https://getdata-real.firebaseio.com",
    projectId: "getdata-real",
    storageBucket: "getdata-real.appspot.com",
    };
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();
/*
let cityRef = db.collection('data-angota').doc('2012033879');
let getDoc = cityRef.get().then(doc => {
    if (!doc.exists) {
      console.log('No such document!');
    } else {
      console.log('Document data:', doc.data());
    }
  }).catch(err => {
    console.log('Error getting document', err);
  });
  */
  db.collection("log-absen").get().then((querySnapshot) => {
    querySnapshot.forEach((doc) => {
        console.log(`${doc.id} => ${doc.data()}`);
    });
});