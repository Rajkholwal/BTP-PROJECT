import React from 'react'
// import { GoogleLogin, GoogleLogout } from 'react-google-login';
import { useState } from 'react';
import UpperNav from './UpperNav';
import QuizForm from './Form';
import { useEffect } from 'react';
import Loading from './Loading';
import './OptionSelector.css';
import engineeringStudentImage from './Student_engineering.png'
import nonEngineeringStudentImage from './Student.webp';
import facultyImage from './Faculty.jpg';
import industryPersonImage from './Industry.jpg';
import './Firstpage.css'

const clientId = '1099148463228-fniq392tv0qv5hlbm084r9m8tp8ph0ls.apps.googleusercontent.com';
const Firstpage = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [loggedInName, setLoggedInName] = useState('')
    const [loggedInEmail, setLoggedInEmail] = useState('')
    const [loading, setLoading] = useState(true)
    const [selectedOption, setSelectedOption] = useState(null);
    const [clickedImage, setClickedImage] = useState(0);
    const feedbackFormLink = "https://docs.google.com/forms/d/1olMjHfmbrhPrhjl35su0kN_OX600hA60nAxo1-BEvlk/edit";
    // const onSuccessLogin = (res) => {
    //     console.log("Login Success current user:")
    //     const { name, email } = res.profileObj
    //     console.log("name: ", name)
    //     console.log("email", email)
    //     setLoggedInEmail(email)
    //     setLoggedInName(name)
    //     setIsLoggedIn(true)
    // }
    // const onFailureLogin = (res) => {
    //     console.log("Login failed", res)
    // }
    // const onSuccessLogout = () => {
    //     console.log("logout done")
    //     setIsLoggedIn(false)
    //     setLoggedInEmail('')
    //     setLoggedInName('')
    // }
    const handleOptionSelect = (option) => {
        setSelectedOption(option);
        if (option === 'student-non-engneering') {
            setClickedImage(1);
        }
    };
    const handleGo = () => {
        if (selectedOption == null) {
            alert('Please select one of the option')
            return
        }
        setLoggedInName('dummy-1')
        setLoggedInEmail('dummy-2')
        setIsLoggedIn(true)
    }

    useEffect(() => {
        // Simulate loading delay (you can replace this with your actual data loading logic)
        setTimeout(() => {
            setLoading(false);
        }, 2000);
    }, []);
    localStorage.clear()
    return (
        <div>
            {
                loading ?
                    <Loading /> :
                    <>
                        <div className="App">
                            {isLoggedIn ? (
                                <div>
                                    {/* Content for authenticated users */}
                                    {/* <UpperNav name={loggedInName} email={loggedInEmail} /> */}
                                    <div className='relative isolate px-60 lg:px-8'>
                                        <div class="mt-5">
                                            <div class="hidden sm:flex sm:justify-center">
                                                {/* <div class=" px-3 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
                                                    <GoogleLogout
                                                        clientId={clientId}
                                                        buttonText="Logout"
                                                        onLogoutSuccess={onSuccessLogout}
                                                    />

                                                </div>
                                                <div class=" px-3 text-sm leading-6 text-gray-600 ring-1 ring-gray-900/10 hover:ring-gray-900/20">
                                                    <GoogleLogin
                                                        clientId={clientId}
                                                        buttonText="Sign in using other account"
                                                        onSuccess={onSuccessLogin}
                                                        onFailure={onFailureLogin}
                                                        cookiePolicy={'single_host_origin'}
                                                        isSignedIn={true}
                                                    />

                                                </div> */}

                                            </div>
                                        </div>
                                    </div>
                                    <QuizForm loggedInName={loggedInName} loggedInEmail={loggedInEmail} loggedInType={selectedOption} />
                                </div>
                            ) : (
                                <div class="bg-white py-24 sm:py-32">
                                    <div className="option-selector-container">
                                        <h2><b>Please Select your category</b></h2>
                                        <div className="options">
                                            <div
                                                className={`option ${selectedOption === 'Engineering Student' ? 'selected' : ''}`}
                                                onClick={() => handleOptionSelect('Engineering Student')}
                                            >
                                                <div className="image-container">
                                                    <img src={engineeringStudentImage} alt="Engineering Student" />
                                                </div>
                                                Engineering Student
                                            </div>
                                            <div
                                                className={`option ${selectedOption === 'Non-Engineering Student' ? 'selected' : ''}`}
                                                onClick={() => handleOptionSelect('Non-Engineering Student')}
                                            >
                                                <div className="image-container">
                                                    <img src={nonEngineeringStudentImage} alt="Non-Engineering Student" />
                                                </div>
                                                Non-Engineering Student
                                            </div>
                                            <div
                                                className={`option ${selectedOption === 'Faculty' ? 'selected' : ''}`}
                                                onClick={() => handleOptionSelect('Faculty')}
                                            >
                                                <div className="image-container">
                                                    <img src={facultyImage} alt="Faculty" />
                                                </div>
                                                Faculty
                                            </div>
                                            <div
                                                className={`option ${selectedOption === 'Industry Person' ? 'selected' : ''}`}
                                                onClick={() => handleOptionSelect('Industry Person')}
                                            >
                                                <div className="image-container">
                                                    <img src={industryPersonImage} alt="Industry Person" />
                                                </div>
                                                Industry Person
                                            </div>
                                        </div>
                                        {/* <p>You selected: {selectedOption}</p> */}
                                        <button
                                            onClick={handleGo}
                                            className="mt-4 ml-8 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                        >
                                            Go!
                                        </button>
                                        <br />
                                    </div>

                                    <div class="mx-auto max-w-7xl px-6 lg:px-8">
                                        <div class="mx-auto max-w-2xl lg:text-center">
                                            <p class="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Attempt Your personalized quiz and assess yourself</p>
                                            <p class="mt-6 text-lg leading-8 text-gray-600 mb-3">We value your feedback! If you encountered any issues or have suggestions to improve the website, please let us know.</p>

                                            {/* <h2 class="text-base font-semibold leading-7 text-indigo-600"><GoogleLogin
                                                clientId={clientId}
                                                buttonText="Sign in with Google"
                                                onSuccess={onSuccessLogin}
                                                onFailure={onFailureLogin}
                                                cookiePolicy={'single_host_origin'}
                                                isSignedIn={true}
                                            /></h2> */}
                                            <div className="feedback-btn-container">
                                                <button
                                                    onClick={() => window.open(feedbackFormLink, '_blank')}
                                                    className="feedback-btn"
                                                >
                                                    Provide Feedback
                                                </button>
                                            </div>
                                        </div>
                                    </div>

                                </div>

                            )}
                        </div>
                    </>
            }
        </div>
    )
}

export default Firstpage
