// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA2XU4XfBzAGRPgAkfnrOX1i5Mqmgs9qmU",
  authDomain: "online-quiz-assessment.firebaseapp.com",
  projectId: "online-quiz-assessment",
  storageBucket: "online-quiz-assessment.firebasestorage.app",
  messagingSenderId: "818171389884",
  appId: "1:818171389884:web:092fafc6013d8a4820adb9",
  measurementId: "G-R44TCF0270"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);