import React from 'react'
// import { GoogleLogin, GoogleLogout } from 'react-google-login';
import { useState } from 'react';
import QuizForm from './Form';
import { useEffect } from 'react';
import Loading from './Loading';
import './OptionSelector.css';
import engineeringStudentImage from './Student_engineering.png'
import facultyImage from './Faculty.jpg';
import './Firstpage.css'

const Firstpage = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [loggedInName, setLoggedInName] = useState('')
    const [loggedInEmail, setLoggedInEmail] = useState('')
    const [loading, setLoading] = useState(true)
    const [selectedOption, setSelectedOption] = useState(null);
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
                                <div className="bg-gray-100 py-16 sm:py-20 text-slate-900">
                                    <div className="mx-auto max-w-6xl px-6 lg:px-8">
                                        <div className="rounded-3xl border border-gray-200 bg-white p-8 shadow">
                                        <h2 className="text-center text-2xl font-bold">Please select your role</h2>
                                        <p className="mt-2 text-center text-slate-600">Choose one to continue</p>

                                        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-2">
                                            <button
                                                type="button"
                                                onClick={() => handleOptionSelect('Engineering Student')}
                                                className={`group rounded-2xl border p-4 text-left shadow-sm transition ${
                                                    selectedOption === 'Engineering Student'
                                                        ? 'border-emerald-600 bg-emerald-50'
                                                        : 'border-gray-200 bg-white hover:bg-gray-50'
                                                }`}
                                            >
                                                <div className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-gray-50 p-3">
                                                    <img src={engineeringStudentImage} alt="Engineering Student" className="h-full w-full object-contain" />
                                                </div>
                                                <div className="mt-4 text-base font-semibold">Engineering Student</div>
                                                <div className="mt-1 text-sm text-slate-600">Core DLD / digital logic track</div>
                                            </button>

                                            <button
                                                type="button"
                                                onClick={() => handleOptionSelect('Faculty')}
                                                className={`group rounded-2xl border p-4 text-left shadow-sm transition ${
                                                    selectedOption === 'Faculty'
                                                        ? 'border-emerald-600 bg-emerald-50'
                                                        : 'border-gray-200 bg-white hover:bg-gray-50'
                                                }`}
                                            >
                                                <div className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-gray-50 p-3">
                                                    <img src={facultyImage} alt="Faculty" className="h-full w-full object-contain" />
                                                </div>
                                                <div className="mt-4 text-base font-semibold">Faculty</div>
                                                <div className="mt-1 text-sm text-slate-600">Create/preview assessments</div>
                                            </button>
                                        </div>

                                        <div className="mt-10 flex justify-center">
                                            <button
                                                onClick={handleGo}
                                                className="rounded-md bg-emerald-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-emerald-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600"
                                            >
                                                Continue
                                            </button>
                                        </div>

                                        <div className="mx-auto mt-14 max-w-2xl text-center">
                                            <p className="text-3xl font-bold tracking-tight">Attempt your personalized quiz and assess yourself</p>
                                            <p className="mt-4 text-lg leading-8 text-slate-600 mb-3">
                                                We value your feedback! If you encountered any issues or have suggestions to improve the website, please let us know.
                                            </p>

                                            {/* <h2 class="text-base font-semibold leading-7 text-indigo-600"><GoogleLogin
                                                clientId={clientId}
                                                buttonText="Sign in with Google"
                                                onSuccess={onSuccessLogin}
                                                onFailure={onFailureLogin}
                                                cookiePolicy={'single_host_origin'}
                                                isSignedIn={true}
                                            /></h2> */}
                                            <div className="mt-6 flex justify-center">
                                                <button
                                                    onClick={() => window.open(feedbackFormLink, '_blank')}
                                                    className="rounded-md bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
                                                >
                                                    Provide feedback
                                                </button>
                                            </div>
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
