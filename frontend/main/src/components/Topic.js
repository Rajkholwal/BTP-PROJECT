import React from 'react'
import QuizForm from './Form'

const Topic = () => {
    return (
        <div class="bg-white py-24 sm:py-32">
            <div class="mx-auto grid max-w-7xl gap-x-8 gap-y-20 px-6 lg:px-8 xl:grid-cols-3">
                <div class="max-w-2xl">
                    <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Meet our leadership</h2>
                    <p class="mt-6 text-lg leading-8 text-gray-600">Libero fames augue nisl porttitor nisi, quis. Id ac elit odio vitae elementum enim vitae ullamcorper suspendisse.</p>
                </div>

                    {/* <li> */}
                            <QuizForm/>

                    {/* </li> */}

                {/* </ul> */}
            </div>
        </div>
    )
}

export default Topic
