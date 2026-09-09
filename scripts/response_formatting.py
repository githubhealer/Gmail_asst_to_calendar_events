response = """      SUBJECT: Got a crazy idea for your city? Build it for ₹1 Crore.
                    SENDER: Ananya Bhatt <noreply@unstop.news>
                    DATE: 2026-09-06T17:41:46+05:30
                    INFORMATION: An email announcing a competition for students to solve urban challenges using Google Gemini with a prize pool of ₹1 Crore.

                    SUBJECT: Do certifications actually help you get hired?
                    SENDER: Tech With Tim <tim@techwithtim.net>
                    DATE: 2026-09-06T17:32:38+05:30
                    INFORMATION: An email discussing whether AI certifications help with job applications and providing a link to a video on 6 AI certifications to consider in 2026.

                    SUBJECT: [Learning Drop] Are you stupid? Because I am.
                    SENDER: Dr. Justin at iCanStudy <drjustinsung@icanstudy.com>
                    DATE: 2026-09-06T17:10:54+05:30
                    INFORMATION: An email about the Dunning-Kruger effect, explaining what it is, how it affects self-perception, and a strategy for identifying knowledge gaps.

                    SUBJECT: Sangam Club Presents UDAY (06-September-2026)
                    SENDER: 'Director Student Welfare, Chennai Campus' via CSE with spl. in A I and Robotics 2023 Group, Chennai Campus <ccbrs23@vitstudent.ac.in>
                    DATE: 2026-09-06T15:57:30+05:30
                    INFORMATION: An invitation to the UDAY event organized by the Sangam Club at Nethaji Auditorium on September 6, 2026, at 5:00 PM.

                    SUBJECT: E-Con Systems next round of selection process is scheduled on 07-09-2026 & 08-09-2026 by 08:30 am @ VIT Chennai campus
                    SENDER: 'No Reply CDC Info' via VITIANS CDC Group, Vellore and Chennai Campus <vitianscdc2027@vitstudent.ac.in>
                    DATE: 2026-09-06T11:25:53+05:30
                    INFORMATION: A reminder for students that the selection process for E-Con Systems will take place at the Chennai campus on September 7th and 8th, 2026.
            """
import re
sub_pattern="SUBJECT:\s*(.*)"
#SENDER:\s*(.*)|DATE:\s*(.*)|INFORMATION:\s*(.*)"
subject = re.findall(sub_pattern,response)
print(subject)