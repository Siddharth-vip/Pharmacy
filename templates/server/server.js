const express = require("express");
const bodyParser = require("body-parser");
const nodemailer = require("nodemailer");
const cors = require("cors");

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Route to handle contact form submission
app.post("/send-message", async (req, res) => {
    const { name, email, subject, message } = req.body;

    try {
        // Set up Nodemailer transport
        const transporter = nodemailer.createTransport({
            service: "gmail",
            auth: {
                user: "siddharthabimanu007@gmail.com", // Replace with your email
                pass: "siddhu020904007", // Replace with your email password
            },
        });

        // Mail options
        const mailOptions = {
            from: email,
            to: "siddharthabimanu007@gmail.com", // Replace with the recipient's email
            subject: `Contact Form Submission: ${subject}`,
            text: `You received a new message from ${name} (${email}):\n\n${message}`,
        };

        // Send mail
        await transporter.sendMail(mailOptions);

        res.status(200).send({ success: true, message: "Message sent successfully!" });
    } catch (error) {
        console.error(error);
        res.status(500).send({ success: false, message: "Failed to send the message." });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
