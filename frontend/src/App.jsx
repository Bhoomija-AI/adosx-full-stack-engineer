import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [orgId, setOrgId] = useState("ORG-A");
  const [reason, setReason] = useState("ALL");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchDiscrepancies = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/discrepancies/?org_id=${orgId}`
      );

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.error || "Something went wrong");
      }

      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDiscrepancies();
  }, [orgId]);

  const filteredResults =
    data?.results.filter(
      (item) => reason === "ALL" || item.reason === reason
    ) || [];

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>Discrepancy Dashboard</h1>
          <p>Monitor and review reconciliation issues</p>
        </div>

        <div className="controls">
          <div className="org-selector">
            <label>Organization</label>

            <select
              value={orgId}
              onChange={(e) => setOrgId(e.target.value)}
            >
              <option value="ORG-A">ORG-A</option>
              <option value="ORG-B">ORG-B</option>
            </select>
          </div>

          <div className="org-selector">
            <label>Reason</label>

            <select
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            >
              <option value="ALL">All</option>
              <option value="VALUE_MISMATCH">Value Mismatch</option>
              <option value="MISSING_IN_SYSTEM_B">
                Missing in System B
              </option>
              <option value="DUPLICATE_IN_SYSTEM_B">
                Duplicate in System B
              </option>
              <option value="ORPHAN_IN_SYSTEM_B">
                Orphan in System B
              </option>
            </select>
          </div>

          <button onClick={fetchDiscrepancies} disabled={loading}>
            {loading ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </header>

      {loading && <div className="message">Loading...</div>}

      {error && <div className="error">{error}</div>}

      {data && !loading && (
        <>
          <div className="summary-card">
            <span>Showing Discrepancies</span>
            <strong>{filteredResults.length}</strong>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Record ID</th>
                  <th>Reason</th>
                  <th>Location</th>
                  <th>Value A</th>
                  <th>Value B</th>
                </tr>
              </thead>

              <tbody>
                {filteredResults.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="message">
                      No discrepancies found.
                    </td>
                  </tr>
                ) : (
                  filteredResults.map((item, index) => (
                    <tr key={`${item.record_id}-${index}`}>
                      <td>{item.record_id}</td>

                      <td>
                        <span
                          className={`badge ${item.reason.toLowerCase()}`}
                        >
                          {item.reason.replaceAll("_", " ")}
                        </span>
                      </td>

                      <td>{item.location_id}</td>

                      <td>
                        {item.value_a !== null && item.value_a !== ""
                          ? item.value_a
                          : "-"}
                      </td>

                      <td>
                        {item.value_b !== null && item.value_b !== ""
                          ? item.value_b
                          : "-"}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
