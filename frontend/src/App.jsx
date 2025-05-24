import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function App() {
  const [myProfile, setMyProfile] = useState('');
  const [theirProfile, setTheirProfile] = useState('');
  const [meetingPurpose, setMeetingPurpose] = useState('');
  const [insight, setInsight] = useState('');
  const [loading, setLoading] = useState(false);

  const generateInsight = async () => {
    setLoading(true);
    const res = await fetch('https://<your-backend-url>/generate-insight', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        my_profile: myProfile,
        their_profile: theirProfile,
        meeting_purpose: meetingPurpose
      })
    });
    const data = await res.json();
    setInsight(data.output);
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">🔗 LinkedinBro: Outreach Helper</h1>

      <div className="grid grid-cols-1 gap-4">
        <textarea
          className="border p-3 rounded w-full"
          placeholder="Paste Your LinkedIn Summary"
          value={myProfile}
          onChange={(e) => setMyProfile(e.target.value)}
          rows={5}
        />
        <textarea
          className="border p-3 rounded w-full"
          placeholder="Paste Their LinkedIn Summary"
          value={theirProfile}
          onChange={(e) => setTheirProfile(e.target.value)}
          rows={5}
        />
        <input
          className="border p-3 rounded w-full"
          placeholder="What’s the meeting about?"
          value={meetingPurpose}
          onChange={(e) => setMeetingPurpose(e.target.value)}
        />
        <button
          className="bg-blue-600 text-white py-2 rounded font-semibold hover:bg-blue-700"
          onClick={generateInsight}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Meeting Insights + Outreach Pack'}
        </button>
      </div>

      {insight && (
        <div className="mt-8 border-t pt-6">
          <ReactMarkdown className="prose prose-lg max-w-none">{insight}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
