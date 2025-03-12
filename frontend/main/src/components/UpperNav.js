import React, { useState, useEffect, useRef } from "react";
import { FaFileSignature } from "react-icons/fa";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { signOut } from "./redux/userSlice";

const UpperNav = (props) => {
    const { name } = props;
    const dispatch = useDispatch();
    const currentUser = useSelector((state) => state.user.currentUser);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setDropdownOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    const handleLogout = () => {
        dispatch(signOut());
        setDropdownOpen(false); // Close dropdown after logout
    };

    return (
        <nav className="bg-gray-800">
            <div className="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
                <div className="relative flex h-16 items-center justify-between">
                    <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                        <div className="flex flex-shrink-0 items-center">
                            <FaFileSignature color="white" />
                        </div>
                        <div className="hidden sm:ml-6 sm:block">
                            <div className="flex space-x-4">
                                <span className="text-gray-300 rounded-md px-3 py-2 text-sm font-medium">
                                    Welcome {currentUser ? currentUser.name : "Guest"}!
                                </span>
                                <Link to="/" className="bg-gray-900 text-white rounded-md px-3 py-2 text-sm font-medium">
                                    Dashboard
                                </Link>
                            </div>
                        </div>
                    </div>
                    <div className="relative flex items-center pr-2">
                        <button className="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white">
                            <span className="sr-only">View notifications</span>
                            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                            </svg>
                        </button>

                        {/* Dropdown Menu */}
                        <div ref={dropdownRef} className="relative">
                            <button
                                className="ml-3 bg-gray-800 text-gray-400 p-2 rounded-md hover:text-white"
                                onClick={() => setDropdownOpen(!dropdownOpen)}
                            >
                                ▼
                            </button>

                            {dropdownOpen && (
                                <div className="absolute right-0 mt-2 w-40 bg-white rounded-md shadow-lg">
                                    {currentUser ? (
                                        <>
                                            <Link
                                                to="/profile"
                                                className="block px-4 py-2 text-gray-700 hover:bg-gray-200"
                                                onClick={() => setDropdownOpen(false)}
                                            >
                                                Profile
                                            </Link>
                                            <button
                                                onClick={handleLogout}
                                                className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-200"
                                            >
                                                Logout
                                            </button>
                                        </>
                                    ) : (
                                        <Link
                                            to="/login-signup"
                                            className="block px-4 py-2 text-gray-700 hover:bg-gray-200"
                                            onClick={() => setDropdownOpen(false)}
                                        >
                                            SignIn-Up
                                        </Link>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default UpperNav;
