import React, { useState } from "react";

function App() {
  const [myProfile, setMyProfile] = useState("");
  const [theirProfile, setTheirProfile] = useState("");
  const [meetingPurpose, setMeetingPurpose] = useState("LinkedIn Outreach");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setOutput("");

    try {
      const response = await fetch("http://localhost:8000/generate-insight", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          my_profile: myProfile,
          their_profile: theirProfile,
          meeting_purpose: meetingPurpose,
        }),
      });

      const data = await response.json();
      if (data.output) {
        setOutput(data.output);
      } else {
        setOutput("No output generated.");
      }
    } catch (error) {
      console.error("Error:", error);
      setOutput("Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">LinkedIn Bro - Outreach Generator</h1>

      <label className="block mb-2 font-semibold">Your Profile Summary</label>
      <textarea
        className="w-full p-3 border rounded mb-4"
        rows="6"
        value={myProfile}
        onChange={(e) => setMyProfile(e.target.value)}
        placeholder="Paste your LinkedIn summary here"
      />

      <label className="block mb-2 font-semibold">Prospect's Profile Summary</label>
      <textarea
        className="w-full p-3 border rounded mb-4"
        rows="6"
        value={theirProfile}
        onChange={(e) => setTheirProfile(e.target.value)}
        placeholder="Paste their LinkedIn summary here"
      />

      <label className="block mb-2 font-semibold">Meeting Purpose</label>
      <input
        type="text"
        className="w-full p-3 border rounded mb-4"
        value={meetingPurpose}
        onChange={(e) => setMeetingPurpose(e.target.value)}
      />

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Insight"}
      </button>

      {output && (
        <div className="mt-8 p-4 bg-gray-100 rounded whitespace-pre-wrap">
          <h2 className="text-xl font-bold mb-2">Output</h2>
          <div>{output}</div>
        </div>
      )}
    </div>
  );
}

export default App;
