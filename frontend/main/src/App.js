import UpperNav from "./components/UpperNav";
import FileList from "./components/Archives";
import { Route, Routes, BrowserRouter } from 'react-router-dom';
import AssessmentPage from "./components/AssessmentPage";
import AssessmentDone from "./components/AssessmentDone";
import Firstpage from "./components/Firstpage";
import Profile from "./components/Profile";
import ReviewAssessment from './components/ReviewAssessment';
import LoginSignup from "./components/LoginSignup";
function App() {
  return (
    <>
    <div className="min-h-screen bg-gray-100 text-slate-900">
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
        {/* <Route element={<PrivateRoute />}> */}

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
        {/* </Route> */}


      </Routes>
      </BrowserRouter>
    </div>
    </>
  );
}

export default App;
