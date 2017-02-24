# load libraries
require(tidyr)
require(dplyr)
require(ggplot2)
require(svglite)

# setwd to this file's directory
setwd(dirname(parent.frame(2)$ofile))

# load data
# specify filepath to csv
fp <- "/Volumes/Data/Research/CDB/openSMILE/adults_speak/adults_speak.csv"
# read csv into `adults` variable as Boolean matrix
adults <- gather(read.csv(fp, header = TRUE, colClasses =
          c(NA, "logical", "logical", "logical", "logical", "logical")),
          cond, adults_speaking, -c(X, SM.dx))
# remove `fp` variable
remove(fp)

# reshape data
colnames(adults)[1] = "URSI"
adults = separate(data=adults, col=cond, into=c("vocal", "stranger"), remove=TRUE)
adults["stranger"] = adults["stranger"] == "w"
adults["vocal"] = adults["vocal"] == "vocal"

# ANOVAs
summary(aov(SM.dx ~ adults_speaking + Error(URSI), data=adults))
summary(aov(vocal ~ adults_speaking + Error(URSI), data=adults))
summary(aov(stranger ~ adults_speaking + Error(URSI), data=adults))
summary(aov(SM.dx ~ (vocal * stranger * adults_speaking) + Error(URSI), data=adults))
summary(aov(adults_speaking ~ (vocal * stranger * SM.dx) + Error(URSI), data=adults))

# Visualize
adults %>%
  group_by(stranger, vocal) %>%
  filter(adults_speaking == TRUE) %>%
  ggplot(aes(x=factor(vocal, labels=c("button press", "vocal")), fill=factor(stranger))) + geom_bar(position="dodge") + guides(fill=guide_legend(title="Stranger Presence")) + labs(title="Adult Vocalizations by Experimental Condition and Stranger Presence", x = "Experimental Condition", y="number of cases in which adults vocalized")
ggsave("images/adults_by_vocal_by_stranger.svg")

adults %>%
  group_by(stranger, vocal) %>%
  filter(adults_speaking == TRUE) %>%
  ggplot(aes(x=factor(stranger), fill=factor(vocal, labels=c("button press", "vocal")))) + geom_bar(position="dodge") + guides(fill=guide_legend(title="Experimental Condition")) + labs(title="Adult Vocalizations by Stranger Presence and Experimental Condition", x = "Stranger Presence", y="number of cases in which adults vocalized")
ggsave("images/adults_by_stranger_by_vocal.svg")