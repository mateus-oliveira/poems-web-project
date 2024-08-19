"use client";

import { useEffect, useState } from 'react';
import api from '@/utils/api';
import { API_COMMENTS, API_LIKES, API_POSTS } from '@/constants/routes';
import getUser from '@/utils/getUser';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHeart } from '@fortawesome/free-solid-svg-icons';
import PoemCard from './PoemCard';

interface User {
  id: number;
  name: string;
  email: string;
};

interface Poem {
  id: number;
  title: string;
  content: string;
  author: User;
};

interface Comment {
  id: number;
  content: string;
  author: User;
};

interface PoemModalProps {
  poem: Poem;
  onClose: () => void;
};


const PostModal = ({ poem, onClose }: PoemModalProps) => {
  const [likes, setLikes] = useState<number>(0);
  const [comments, setComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [commentText, setCommentText] = useState<string>("");
  const [user, setUser] = useState<User>();
  const [author, setAuthor] = useState<User>();
  const [hasLiked, setHasLiked] = useState<boolean>(false);

  useEffect(() => {
    const user = getUser();
    setUser(user);
    fetchAuthor();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [likesData, commentsData] = await Promise.all([
          api.get<object>(`${API_POSTS}/${poem.id}${API_LIKES}`),
          api.get<Comment[]>(`${API_POSTS}/${poem.id}${API_COMMENTS}`),
        ]);

        setLikes(likesData?.length ?? 0);
        setComments(commentsData);

        const userHasLiked = likesData?.some((like: any) => like.user_id === user?.id);

        setHasLiked(userHasLiked ?? false);
      } catch (error) {
        console.log('Error when trying loading comments', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [poem.id, user?.id]);

  const handleLike = async () => {
    try {
      await api.post(`${API_POSTS}/${poem.id}${API_LIKES}`);
      if (hasLiked) {
        setLikes(likes - 1);
        setHasLiked(false);
      } else {
        setLikes(likes + 1);
        setHasLiked(true);
      }
    } catch (error) {
      console.log('Error when trying like post', error);
    }
  };

  const fetchAuthor = async () => {
    try {
      const data = await api.get(`${API_POSTS}/${poem.id}`);
      setAuthor(data.author);
    } catch (error) {
      console.log(error);
    }
  };

  const handleComment = async () => {
    if (commentText.trim() === "") return;
    try {
      const newComment = await api.post<Comment>(`${API_POSTS}/${poem.id}${API_COMMENTS}`, { content: commentText });
      newComment.author = user;
      setComments([...comments, newComment]);
      setCommentText("");
    } catch (error) {
      console.log('Erro ao comentar no post', error);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 text-black">
      <div className="bg-white rounded-lg overflow-hidden shadow-lg w-full max-w-3xl relative">
        <PoemCard detailed={true} poem={poem} onClick={onClose} />
        <div className="flex">
          <div className="p-4 w-1/2">
            <h2 className="text-xl font-bold">{author?.name}</h2>
            <button
              onClick={handleLike}
              className={`${hasLiked ? 'text-red-500' : 'text-grey-100'} mt-4 flex items-center`}
            >
              <FontAwesomeIcon icon={faHeart} className="mr-2"/>
              ({likes})
            </button>
            <div className="mt-4">
              <input
                type="text"
                placeholder="Add a comment..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                className="border rounded p-2 w-full"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleComment();
                  }
                }}
              />
              <div className="mt-2">
                {comments.map(comment => {
                  return(
                  <div key={comment.id} className="mt-1">
                    <strong>{comment?.author?.name}</strong>: {comment.content}
                  </div>
                )})}
              </div>
            </div>
          </div>
        </div>
        <button
          onClick={onClose}
          className="absolute top-0 right-0 m-4 text-2xl font-bold"
        >
          &times;
        </button>
      </div>
    </div>
  );
};

export default PostModal;
