import Aurora from "./Aurora/Aurora"
import Navbar from "./navbar"

export default function GuidePage() {
  const steps = [
    {
      number: 1,
      title: 'Enter Job Description',
      description: 'Provide detailed information about the position',
      details: [
        'Required skills and competencies',
        'Years of experience needed',
        'Educational requirements',
        'Job responsibilities',
        'Technical requirements',
        'Soft skills desired'
      ],
      icon: '📝'
    },
    {
      number: 2,
      title: 'Upload CVs',
      description: 'Upload all candidate resumes for this position',
      details: [
        'PDF format supported',
        'Multiple files can be uploaded',
        'Drag and drop or click to browse',
        'All CVs for this specific job posting'
      ],
      icon: '📄'
    },
    {
      number: 3,
      title: 'Analyze CVs',
      description: 'AI-powered analysis matches candidates to job requirements',
      details: [
        'Automatic parsing of CV content',
        'Skills extraction and matching',
        'Experience evaluation',
        'Education verification',
        'Intelligent scoring algorithm'
      ],
      icon: '🔍'
    },
    {
      number: 4,
      title: 'View Ranked Results',
      description: 'Review candidate rankings with detailed insights',
      details: [
        'Candidates ranked by match score',
        'Detailed match explanation',
        'Strengths and weaknesses analysis',
        'Skills gap identification',
        'Experience alignment report'
      ],
      icon: '📊'
    }
  ]

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Aurora Background */}
      <div className="absolute inset-0 z-0">
        <Aurora
          colorStops={[  '#C8ACD6', '#433D8B',]}
          blend={0.5}
          amplitude={1.0}
          speed={0.5}
        />
      </div>

      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 pt-28">
        {/* Introduction */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-extrabold text-white mb-4">
            Find Your Perfect Candidate in 4 Simple Steps
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Our AI-powered platform streamlines your recruitment process by intelligently 
            matching candidates to your job requirements.
          </p>
        </div>

        {/* Steps */}
        <div className="space-y-12">
          {steps.map((step, index) => (
            <div
              key={step.number}
              className="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-700"
            >
              <div className="flex flex-col md:flex-row">
                {/* Step Number Circle */}
                <div className="bg-gradient-to-br from-purple-600 to-purple-800 p-8 md:p-12 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-6xl mb-2">{step.icon}</div>
                    <div className="w-20 h-20 bg-gray-900 rounded-full flex items-center justify-center mx-auto">
                      <span className="text-4xl font-bold text-purple-400">
                        {step.number}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Step Content */}
                <div className="flex-1 p-8 md:p-12">
                  <h3 className="text-2xl font-bold text-white mb-3">
                    {step.title}
                  </h3>
                  <p className="text-lg text-gray-300 mb-6">
                    {step.description}
                  </p>
                  
                  <div className="bg-purple-900/30 border border-purple-700/50 rounded-lg p-6">
                    <h4 className="font-semibold text-purple-300 mb-3">
                      What to include:
                    </h4>
                    <ul className="space-y-2">
                      {step.details.map((detail, i) => (
                        <li key={i} className="flex items-start">
                          <svg
                            className="w-5 h-5 text-purple-400 mr-3 mt-0.5 flex-shrink-0"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                              clipRule="evenodd"
                            />
                          </svg>
                          <span className="text-gray-300">{detail}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>

              {/* Arrow Connector (except for last step) */}
              {index < steps.length - 1 && (
                <div className="flex justify-center py-6">
                  <div className="text-4xl text-purple-400">↓</div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center bg-gradient-to-r from-purple-600 to-purple-800 rounded-2xl p-12 text-white">
          <h3 className="text-3xl font-bold mb-4">
            Ready to Get Started?
          </h3>
          <p className="text-xl mb-8 text-purple-100">
            Start matching candidates to your job openings today!
          </p>
          <a
            href="#matching"
            className="inline-block bg-white text-purple-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-purple-50 transition-colors duration-200 shadow-lg"
          >
            Try MatchaCV Now →
          </a>
        </div>

        {/* Additional Features */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center p-6 bg-gray-800/30 rounded-xl border border-gray-700">
            <div className="text-4xl mb-4">⚡</div>
            <h4 className="font-bold text-white mb-2">Fast & Efficient</h4>
            <p className="text-gray-300">
              Save hours of manual CV screening with AI-powered automation
            </p>
          </div>
          <div className="text-center p-6 bg-gray-800/30 rounded-xl border border-gray-700">
            <div className="text-4xl mb-4">🎯</div>
            <h4 className="font-bold text-white mb-2">Accurate Matching</h4>
            <p className="text-gray-300">
              Advanced algorithms ensure the best candidates rise to the top
            </p>
          </div>
          <div className="text-center p-6 bg-gray-800/30 rounded-xl border border-gray-700">
            <div className="text-4xl mb-4">📈</div>
            <h4 className="font-bold text-white mb-2">Detailed Insights</h4>
            <p className="text-gray-300">
              Understand exactly why each candidate matches or doesn't match
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 bg-black/50 backdrop-blur-sm border-t border-gray-800 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-gray-400">
              © 2025 MatchaCV. Making recruitment smarter.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
