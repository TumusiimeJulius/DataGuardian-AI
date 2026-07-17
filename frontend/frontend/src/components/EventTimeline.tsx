interface Event {
  time: string;
  message: string;
}

export default function EventTimeline({
  events,
}: {
  events: Event[];
}) {
  return (
    <div
      style={{
        background: "#1e293b",
        borderRadius: 15,
        padding: 20,
      }}
    >
      <h2>📜 Live Investigation Timeline</h2>

      <div
        style={{
          marginTop: 20,
        }}
      >
        {events.map((event, index) => (
          <div
            key={index}
            style={{
              marginBottom: 18,
              borderLeft: "3px solid #3b82f6",
              paddingLeft: 15,
            }}
          >
            <small
              style={{
                color: "#94a3b8",
              }}
            >
              {event.time}
            </small>

            <div>{event.message}</div>
          </div>
        ))}
      </div>
    </div>
  );
}