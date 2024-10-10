import React, { useState } from 'react'

const TagSelection = ({availableTags}) => {
    const [selectedTags, setSelectedTags] = useState([])
    const handleTagClick = (tag) => {
        if (selectedTags.includes(tag)) {
            setSelectedTags(selectedTags.filter((selectedTag) => selectedTag !== tag))
        }
        else {
            setSelectedTags([...selectedTags, tag]);
        }
    }
    return (
        <div className="p-4">
            <h2 className="text-xl font-bold mb-4">Please Select Tags</h2>
            <div className="space-x-2">
                {availableTags.map((tag) => (
                    <span
                        key={tag}
                        className={`inline-block px-3 py-1 text-sm font-semibold rounded-full cursor-pointer ${selectedTags.includes(tag) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'
                            }`}
                        onClick={() => handleTagClick(tag)}
                    >
                        {tag}
                    </span>
                ))}
            </div>
            {/* <div className="mt-4">
                <p className="text-gray-700">Selected Tags: {selectedTags.join(', ')}</p>
            </div> */}
        </div>
    );
}

export default TagSelection
