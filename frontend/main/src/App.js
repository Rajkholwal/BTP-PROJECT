import UpperNav from "./components/UpperNav";
// import TagSelection from "./components/TagSelection";
// import LevelSelector from "./components/LevelSelection";
// import QuestionInput from "./components/QuestionInput";
// import QuizForm from "./components/Form";
import FileList from "./components/Archives";
// import Topic from "./components/Topic";
import { Route, Routes,BrowserRouter } from 'react-router-dom';
import AssessmentPage from "./components/AssessmentPage";
import AssessmentDone from "./components/AssessmentDone";
import { gapi } from 'gapi-script'
import { useState, useEffect } from "react";
// import Login from "./components/Login";
// import Logout from "./components/Logout";
import Firstpage from "./components/Firstpage";
import Profile from "./components/Profile";
import ReviewAssessment from './components/ReviewAssessment';
import LoginSignup from "./components/LoginSignup";
import PrivateRoute from "./components/PrivateRoute";
const clientId = '1099148463228-fniq392tv0qv5hlbm084r9m8tp8ph0ls.apps.googleusercontent.com';
function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  // useEffect(() => {
  //   function start() {
  //     gapi.client.init({
  //       clientId: clientId,
  //       scope: ""
  //     }).then(function () {
  //       setIsLoggedIn(true)
  //     })
  //   }
  //   gapi.load('client:auth2', start)
  // })

  return (
    <>
    <BrowserRouter>
     <UpperNav/>
      <Routes>
        <Route path='/' index element={
          <>
            <Firstpage />
          </>
        } />
        <Route path='/past-questions' index element={
          <>
            {/* <UpperNav /> */}
            <FileList />
          </>
        } />
        {/* <Route path='/team' index element={
          <>
            <UpperNav />
          </>
        } /> */}
          <Route path='/profile' index element={
            <>
              <Profile />
            </>
          } />
        <Route path='/login-signup' index element={
          <>
            <LoginSignup />
          </>

        } />
        <Route element={<PrivateRoute />}>

          <Route path='/AssessmentPage' index element={
            <>
              <AssessmentPage />
            </>
          } />
          
          <Route path='/AssessmentDone' index element={
            <>
              <AssessmentDone />
            </>
          } />
          <Route path='/review-assessment' index element={
            <>
              <ReviewAssessment />
            </>

          } />
        </Route>


      </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
