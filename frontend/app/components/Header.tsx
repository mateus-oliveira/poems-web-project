import { CREATE_POEM, LOGIN, DESK } from '@/constants/routes';
import { TOKEN, USER } from '@/constants/storage';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSignOut, faPen } from '@fortawesome/free-solid-svg-icons';


const Header = () => {
  const router = useRouter();

  const handleCreatePoem = () => {
    router.push(CREATE_POEM);
  };

  const handleDesk = () => {
    router.push(DESK);
  };

  const handleLogout = () => {
    localStorage.removeItem(TOKEN);
    localStorage.removeItem(USER);
    router.push(LOGIN);
  };

  return (
    <header className="bg-blue-500 text-white p-4 flex justify-between items-center mb-20">
      <h1 className="text-xl font-bold">FeenixAI - Poems</h1>
      <div>
        <button
          onClick={handleCreatePoem}
          className="bg-white text-blue-500 px-4 py-2 rounded mr-5"
        >
          Create <FontAwesomeIcon icon={faPlus} className="mr-2"/>
        </button>
        <button
          onClick={handleDesk}
          className="bg-white text-blue-500 px-4 py-2 rounded mr-5"
        >
          Poem Desk <FontAwesomeIcon icon={faPen} className="mr-2"/>
        </button>
        <button
          onClick={handleLogout}
          className="bg-white text-blue-500 px-4 py-2 rounded"
        >
          Sign Out <FontAwesomeIcon icon={faSignOut} className="mr-2"/>
        </button>
      </div>
    </header>
  );
};


export default Header;
