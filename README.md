# Automation
Scripts that I use to simplify my work in the microscopy core facility in the Douglas Hospital (MCMP).

PPMS is a microscopy SaaS we use for booking and finances. The **PPMS scripts** interface with the website through the PPMS management utility API (PUMAPI). These scripts analyse microscope usage in some cases and are also used to upload server usage data to the website for server billing.

**Autoshutdown** is an IoT (Internet of Things) routine that checks whether a batch scan was performed under the Autosthudown account of our Olympus VS120 Slide Scanner. If so, it will perform an automatic shutdown of the system, first by remotely shutting down the computer, then by cutting off power from all components using an mPower Pro Ethernet-connected powerstrip. Contact me for details on how to implement this.
