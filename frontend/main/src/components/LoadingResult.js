import React from 'react'
import './Loading.css'

const LoadingResult = () => {
    return (
        <div className="loading-container">
            <div className="spinner"></div>
            <p>Calculating your marks...</p>
        </div>
    )
}

export default LoadingResult
