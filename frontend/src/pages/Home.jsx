import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-2xl text-center">
        {/* Logo/Ícone Educacional */}
        <div className="mx-auto h-24 w-24 bg-gradient-to-r from-blue-500 to-green-500 rounded-full flex items-center justify-center shadow-lg mb-6">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        
        <h1 className="text-4xl font-extrabold text-gray-900 mb-4">
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-green-600">
            Missão Aprendizado
          </span>
        </h1>
        
        <p className="text-lg text-gray-700 max-w-2xl mx-auto">
          Transforme seu aprendizado em uma aventura! Complete desafios, colete conquistas e 
          <span className="font-semibold text-blue-600"> evolua</span> seu conhecimento de forma divertida.
        </p>
        
        {/* Destaques */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-blue-500">
            <h3 className="font-bold text-blue-600">+100 Desafios</h3>
            <p className="text-sm text-gray-600">Conteúdo para todos os níveis</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-green-500">
            <h3 className="font-bold text-green-600">Recompensas</h3>
            <p className="text-sm text-gray-600">Ganhe pontos e medalhas</p>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-md border-l-4 border-purple-500">
            <h3 className="font-bold text-purple-600">Ranking</h3>
            <p className="text-sm text-gray-600">Competição saudável</p>
          </div>
        </div>
      </div>

      <div className="mt-12 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-xl rounded-2xl border border-gray-100">
          <h2 className="text-center text-2xl font-bold text-gray-800 mb-6">
            Comece sua jornada
          </h2>
          
          <div className="space-y-4">
            <Link
              to="/login"
              className="w-full flex items-center justify-center py-3 px-4 rounded-xl shadow-sm text-lg font-medium text-white bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 transition-all"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
              </svg>
              Entrar na minha conta
            </Link>
            
            <Link
              to="/register"
              className="w-full flex items-center justify-center py-3 px-4 rounded-xl shadow-sm text-lg font-medium text-blue-600 bg-white border-2 border-blue-100 hover:border-blue-200 hover:bg-blue-50 transition-all"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Criar nova conta
            </Link>
          </div>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Conecte-se e comece a aprender hoje mesmo!
            </p>
          </div>
        </div>
      </div>
      
      {/* Rodapé Educacional */}
      <div className="mt-12 text-center">
        <p className="text-sm text-gray-500">
          Desenvolvido para <span className="font-semibold text-blue-500">aprendizado ativo</span> e <span className="font-semibold text-green-500">engajamento</span>
        </p>
      </div>
    </div>
  );
}