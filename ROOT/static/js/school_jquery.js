$(document).ready(function(){
  $('#id_SCHOOL_NAME').on('change', function(){
     console.log($('#id_SCHOOL_NAME').val());
      $('#id_PROGRAM_NAME').html('');
      if($('#id_SCHOOL_NAME').val()=='School_of_Technology'){
          $('#id_PROGRAM_NAME').append('<option value="Chemical_Engineering">Chemical Engineering</option>');
          $('#id_PROGRAM_NAME').append('<option value="Mechanical_Engineering">Mechanical Engineering</option>');
          $('#id_PROGRAM_NAME').append('<option value="Computer_Science_and_Engineering">Computer Science and Engineering</option>');
          $('#id_PROGRAM_NAME').append('<option value="Fire_and_Safety_Engineering">Fire and Safety Engineering</option>');
      }
      else if($('#id_SCHOOL_NAME').val()=='School_of_Science'){
          $('#id_PROGRAM_NAME').append('<option value="Chemistry_HONS">Chemistry HONS</option>');
          $('#id_PROGRAM_NAME').append('<option value="Biotechnology_HONS">Biotechnology HONS</option>');
          $('#id_PROGRAM_NAME').append('<option value="Industrial_Chemistry_HONS">Industrial Chemistry HONS</option>');
          $('#id_PROGRAM_NAME').append('<option value="Micro_Biology_HONS">Micro Biology HONS</option>');
          $('#id_PROGRAM_NAME').append('<option value="Chemistry_MSC">Chemistry MSC</option>');
          $('#id_PROGRAM_NAME').append('<option value="Biotechnology_MSC">Biotechnology MSC</option>');
          $('#id_PROGRAM_NAME').append('<option value="Industrial_Chemistry_MSC">Industrial Chemistry MSC</option>');
          $('#id_PROGRAM_NAME').append('<option value="Chemistry_PHD">Chemistry PHD</option>');
          $('#id_PROGRAM_NAME').append('<option value="Biotechnology_PHD">Biotechnology PHD</option>');

      }
      else if($('#id_SCHOOL_NAME').val()=='School_of_Management'){
          $('#id_PROGRAM_NAME').append('<option value="General">General</option>');
          $('#id_PROGRAM_NAME').append('<option value="Business_Analytics">Business Analytics</option>');
      }
  });
});
