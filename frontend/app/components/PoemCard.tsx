import React from 'react';


const PoemCard = ({poem, onClick, detailed=false}) => {
    return (
        <div 
            key={poem.id} 
            onClick={onClick}
            className="cursor-pointer mt-4 w-96 mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
            <div className="px-6 py-4">
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{poem.title}</h3>
              <p className="text-gray-600 text-base whitespace-pre-line">{detailed ? poem.content : "See more..."}</p>
            </div>
        </div>
    )
}

export default PoemCard;
