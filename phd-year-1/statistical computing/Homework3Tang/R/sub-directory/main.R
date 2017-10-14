library(methods)
library(dplyr)
library(tidyr)
library(readr)
library(magrittr)

setClass("LongitudinalData", slots = c(id = "numeric",
                                       visit = "numeric",
                                       room = "character",
                                       value = "numeric",
                                       timepoint = "numeric")
)

setClass("ld_project", representation(s="numeric", v="numeric", r="character"),
         contains = "LongitudinalData",
         prototype(s=NA_real_, v=NA_integer_, r=NA_character_))

setClass("ld_summary", representation(summary_array = "numeric",
                                      summary_table = "data.frame"),
         prototype(summary_array = c()))

#make_LD  subject  visit  room
setGeneric("make_LD", function(data) {
  standardGeneric("make_LD")
})
setMethod("make_LD", "data.frame", 
          function(data){
            new("LongitudinalData", 
                id = as.numeric(data["id"]$id),
                visit = as.numeric(data["visit"]$visit),
                room = as.character(data["room"]$room),
                value = as.numeric(data["value"]$value),
                timepoint = as.numeric(data["timepoint"]$timepoint))
          })

setMethod("print", "LongitudinalData", 
          function(x, ...) {
            cat(sprintf("Longitudinal dataset with %d subjects\n", length(unique(x@id))))        
          })

setMethod("print", "ld_project", 
          function(x, ...) {
            s = x@s
            v = x@v
            r = x@r
            if(!is.na(s) & is.na(v) & is.na(r)){
              if(length(x@id) > 0) cat(sprintf("Subject ID: %s\n", s))
              else cat("NULL\n")
            }
            else{
              if(!is.na(s)) cat(sprintf("ID: %s\n", s))
              if(!is.na(v)) cat(sprintf("Visit: %s\n", v))
              if(!is.na(r)) cat(sprintf("Room: %s\n", r))
            }
            if(is.na(s) & is.na(s) & is.na(s)) cat("NULL\n")
          })

setMethod("print", "ld_summary", 
          function(x, ...) {
            n = length(x@summary_array)
            if(n == 1){
              cat(sprintf("%s: %s\n", names(x@summary_array), x@summary_array[1]))
              print(x@summary_table)
            }
            else{
              cat(sprintf("%s: %s\n", names(x@summary_array)[1], x@summary_array[1]))
              print(x@summary_array[2:n])
            }
          })

setGeneric("subject", function(data, id) {
  standardGeneric("subject")
})
setMethod("subject", "ld_project", 
          function(data, id) {
            out = new("ld_project")
            out@s = id
            if(!is.na(data@v)) out@v = data@v
            if(!is.na(data@r)) out@r = data@r
            out@id = data@id[data@id == id]
            out@visit = data@visit[data@id == id]
            out@room = data@room[data@id == id]
            out@value = data@value[data@id == id]
            out@timepoint = data@timepoint[data@id == id]
            return(out)
          })
setMethod("subject", "LongitudinalData",
          function(data, id){
            aux = new("ld_project", id = data@id,
                      visit = data@visit,
                      room = data@room,
                      value = data@value,
                      timepoint = data@timepoint)
            subject(aux, id)
          })

setGeneric("visit", function(data, visit) {
  standardGeneric("visit")
})
setMethod("visit", "ld_project", 
          function(data, visit) {
            out = new("ld_project")
            out@v = visit
            if(!is.na(data@s)) out@s = data@s
            if(!is.na(data@r)) out@r = data@r
            out@id = data@id[data@visit == visit]
            out@visit = data@visit[data@visit == visit]
            out@room = data@room[data@visit == visit]
            out@value = data@value[data@visit == visit]
            out@timepoint = data@timepoint[data@visit == visit]
            return(out)
          })
setMethod("visit", "LongitudinalData",
          function(data, visit){
            aux = new("ld_project", id = data@id,
                      visit = data@visit,
                      room = data@room,
                      value = data@value,
                      timepoint = data@timepoint)
            visit(aux, visit)
          })

setGeneric("room", function(data, room) {
  standardGeneric("room")
})
setMethod("room", "ld_project", 
          function(data, room) {
            out = new("ld_project")
            out@r = room
            if(!is.na(data@s)) out@s = data@s
            if(!is.na(data@v)) out@v = data@v
            out@id = data@id[data@room == room]
            out@visit = data@visit[data@room == room]
            out@room = data@room[data@room == room]
            out@value = data@value[data@room == room]
            out@timepoint = data@timepoint[data@room == room]
            return(out)
          })
setMethod("room", "LongitudinalData",
          function(data, room){
            aux = new("ld_project", id = data@id,
                      visit = data@visit,
                      room = data@room,
                      value = data@value,
                      timepoint = data@timepoint)
            room(aux, room)
          })

setMethod("summary", "ld_project",
          function(object){
            data = object
            s = data@s
            v = data@v
            r = data@r
            
            out = new("ld_summary")
            
            if(!is.na(s) & is.na(v) & is.na(r)){
              out@summary_array = c(out@summary_array, s)
              names(out@summary_array) = c(names(out@summary_array), "ID")
              
              d = data.frame(visit = data@visit, room = data@room, value = data@value)
              out@summary_table = d %>% 
                group_by(visit,room) %>% 
                summarize(mean = mean(value)) %>%
                spread(room, mean) %>% 
                data.frame()
              return(out)
            }
            else if(!is.na(s) & !is.na(v) & !is.na(r)){
              out@summary_array = c(out@summary_array, s)
              names(out@summary_array)[1] = "ID"
              
              out@summary_array = c(out@summary_array, min(data@value))
              names(out@summary_array)[2] = "Min."
              
              out@summary_array = c(out@summary_array, quantile(data@value, 0.25))
              names(out@summary_array)[3] = "1st Qu."
              
              out@summary_array = c(out@summary_array, median(data@value))
              names(out@summary_array)[4] = "Median"
              
              out@summary_array = c(out@summary_array, mean(data@value))
              names(out@summary_array)[5] = "Mean"
              
              out@summary_array = c(out@summary_array, quantile(data@value, 0.75))
              names(out@summary_array)[6] = "3rd Qu."
              
              out@summary_array = c(out@summary_array, max(data@value))
              names(out@summary_array)[7] = "Max."
              
              return(out)
            }
            else{
              stop("The question didn't specify what should be done in this situation\n")
            }
          })
