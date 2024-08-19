import React, { useEffect, useState } from 'react';
import swal from 'sweetalert';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEdit } from '@fortawesome/free-solid-svg-icons';
import { API_POEMS } from '@/constants/routes';
import api from '@/utils/api';
import getUser from '@/utils/getUser';


interface User {
  id: number;
  name: string;
  email: string;
};

const PoemCard = ({ poem, onClick, detailed = false }) => {
  const [user, setUser] = useState<User>();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editedTitle, setEditedTitle] = useState(poem.title);
  const [editedContent, setEditedContent] = useState(poem.content);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const user = getUser();
    setUser(user);
  }, []);

  const handleEditClick = () => {
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  const handleSaveChanges = async () => {
    
    try {
      await api.put(`${API_POEMS}/${poem.id}`, {title: editedTitle, content: editedContent});
      swal("Success!", "Poem already updated", "success");
      handleModalClose();
    } catch (error) {
      setError('Error when trying create poem');
    } 
  };

  return (
    <div 
      key={poem.id} 
      className="mt-4 w-96 mx-auto bg-white shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4 flex justify-between items-center">
        <div onClick={onClick} className="cursor-pointer" >
          <h3 className="text-xl font-semibold text-gray-800 mb-2">{poem.title}</h3>
          <p className="text-gray-600 text-base whitespace-pre-line">{detailed ? poem.content : "See more..."}</p>
        </div>
        {user?.id === poem?.author_id && (
          <button onClick={handleEditClick} className="ml-4 text-blue-500 hover:text-blue-700">
            <FontAwesomeIcon icon={faEdit} />
          </button>
        )}
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 text-black">
          <div className="bg-white p-6 rounded shadow-lg w-1/3">
            <h2 className="font-bold text-2xl mb-4">Edit Poem</h2>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="title">
                Title
              </label>
              <input
                type="text"
                id="title"
                value={editedTitle}
                onChange={(e) => setEditedTitle(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="content">
                Content
              </label>
              <textarea
                id="content"
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                required
              />
            </div>
            {error && <div className="text-red-500 mb-4">{error}</div>}
            <div className="flex justify-end">
              <button
                onClick={handleModalClose}
                className="bg-gray-500 text-white px-4 py-2 rounded mr-2"
              >
                Cancel
              </button>
              <button
                onClick={handleSaveChanges}
                className="bg-blue-500 text-white px-4 py-2 rounded"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PoemCard;
