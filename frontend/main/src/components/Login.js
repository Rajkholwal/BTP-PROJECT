// import React from 'react'
// import { useState } from 'react'
// import { GoogleLogin } from 'react-google-login'
// import UpperNav from './UpperNav';

// // ID for google authentication
// const clientId = '1099148463228-fniq392tv0qv5hlbm084r9m8tp8ph0ls.apps.googleusercontent.com';

// const Login = ({ onLoginSuccess }) => {

//     const [isLoggedIn, setIsLoggedIn] = useState(false)
//     const [loggedInName, setLoggedInName] = useState('')
//     const [loggedInEmail, setLoggedInEmail] = useState('')

//     const onSuccess = (res) => {
//         console.log("Login Success current user:")
//         const { name, email } = res.profileObj
//         console.log("name: ", name)
//         console.log("email", email)
//         setLoggedInEmail(email)
//         setLoggedInName(name)
//         setIsLoggedIn(true)
//     }
//     const onFailure = (res) => {
//         console.log("Login failed", res)
//     }

//     return (
//         <div>
//             <GoogleLogin
//                 clientId={clientId}
//                 buttonText="Sign in with Google"
//                 onSuccess={onSuccess}
//                 onFailure={onFailure}
//                 cookiePolicy={'single_host_origin'}
//                 isSignedIn={true}
//             />
//             {isLoggedIn ? (
//                 <div>
//                     <b>Welcome: </b>{loggedInName}
//                     <br/>
//                     <b>Current Logged In Email: </b>{loggedInEmail}
//                     <UpperNav name={loggedInName} email={loggedInEmail}/>
//                 </div>
                
                
//             ) : (
//                 <div>
//                     {loggedInEmail}
//                 </div>
//             )}
//         </div>)
// };

// export default Login;
