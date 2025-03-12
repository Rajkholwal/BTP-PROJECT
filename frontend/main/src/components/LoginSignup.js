import React from "react";
import { FcGoogle } from "react-icons/fc";
import { GoogleAuthProvider, signInWithPopup, getAuth } from "firebase/auth";
import { app } from "./firebase";
import { useDispatch } from "react-redux";
import { signInSuccess } from "./redux/userSlice";
import { useNavigate } from "react-router-dom";
const LoginSignup = () => {
    const auth = getAuth(app);
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const handleGoogleClick = async () => {
        const provider = new GoogleAuthProvider();
        
        provider.setCustomParameters({ prompt: "select_account" });
        try {
          const resultsFromGoogle = await signInWithPopup(auth, provider);
          const res = await fetch(`${process.env.REACT_APP_API_URL}/auth/google`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              name: resultsFromGoogle.user.displayName,
              email: resultsFromGoogle.user.email,
              googlePhotoUrl: resultsFromGoogle.user.photoURL,
            }),
          });
        console.log(resultsFromGoogle);
          const data = await res.json();
          if (res.ok) {
            dispatch(signInSuccess(data));
            navigate("/");
          }
        } catch (error) {
          console.log(error);
        }
      };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-blue-400 to-purple-500">
            <div className="bg-white p-8 rounded-2xl shadow-lg max-w-sm text-center">
                <h1 className="text-3xl font-bold text-gray-800 mb-4">Welcome to EduPlatform</h1>
                <p className="text-gray-600 mb-6">Sign in or sign up using your Google account</p>
                <button 
                    onClick={handleGoogleClick} 
                    className="flex items-center justify-center w-full bg-white border border-gray-300 text-gray-700 py-3 px-6 rounded-lg shadow hover:shadow-lg transition-transform transform hover:scale-105"
                >
                    <FcGoogle className="text-2xl mr-2" />
                    Continue with Google
                </button>
            </div>
        </div>
    );
};

export default LoginSignup;
