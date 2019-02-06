/**
 * @Autor Danny Romero
 * @Version 1.0
 * @Proposito Manipulacion de formsets dinamicos para Django
 */

;(function ($){
    $.fn.mensaje = function(opts){
        var options = $.extend( {}, $.fn.mensaje.defaults, opts ); // variable de opciones
        var totalForms = $('#id_' + options.prefix + '-TOTAL_FORMS'); 
        var minForms = $('#id_' + options.prefix + '-MIN_NUM_FORMS');
        var maxForms = $('#id_' + options.prefix + '-MAX_NUM_FORMS');
        var elemBase = totalForms.parent();

        maxForms.after('<input type="hidden" name="'+options.prefix+'-TOT-VIS_FORMS" id="id_'+options.prefix+'-TOT-VIS_FORMS">')
        var totalVisibleForms = $('#id_' + options.prefix + '-TOT-VIS_FORMS');
        totalVisibleForms.val($("#"+elemBase.attr('id')+" input[type='checkbox'][id$='-DELETE']:not([checked])").length)

        /**
         * Crear boton eliminar formulario
         */
        var addBotonEliminar = function(){
            $("#"+elemBase.attr('id')+" input[id$='-DELETE']").each(function(){
                $(this).after("<input type='button' value='"+options.nameButtonDelete+"' id='_"+$(this).attr('id')+"'>")
                $(this).hide()
            })
            $("[for$='-DELETE']").remove()
        }

        /**
         * Crear boton Agregar formulario
         */
        var addBotonAgregar = function(){
            $("#"+elemBase.attr('id')).append("<div class='buttonContent'></div>")
            $("#"+elemBase.attr('id')+"> .form:last").clone(true, true).append(".buttonContent")
            $("#"+elemBase.attr('id')+" .buttonContent").html('<input type="button" value="'+options.nameButton+'" id="buttonAdd'+options.prefix+'"/>')
        }

        /**
         * Darle visibilidad dentro del DOM a boton eliminar
         */
        var showBotonEliminar = function(){
            if(parseInt(minForms.val()) & parseInt(totalVisibleForms.val()) <= parseInt(minForms.val())){
                $("#"+elemBase.attr('id')+" [type='button'][id$='-DELETE']").hide()
            }else if(parseInt(totalVisibleForms.val()) < 2){
                $("#"+elemBase.attr('id')+" [type='button'][id$='-DELETE']").hide()
            }else{
                $("#"+elemBase.attr('id')+" [type='button'][id$='-DELETE']").show()
            }   
        }

        /**
         * Darle visibilidad dentro del DOM a boton agregar
         */
        var showBotonAgregar = function(){
            if(parseInt(maxForms.val()) & parseInt(totalVisibleForms.val()) >= parseInt(maxForms.val())){
                $("#"+elemBase.attr('id')+" #buttonAdd"+options.prefix).hide()
            }else{
                $("#"+elemBase.attr('id')+" #buttonAdd"+options.prefix).show()
            }   
        }

        /**
         * Oculta los formularios para que django se encargue de eliminarlos
         * @param button es el elemento de boton donde se genero el click
         */
        var deleteForms = function(button){
            $("#"+elemBase.attr('id')+" input[type='checkbox'][id='"+button.attr('id').slice(1)+"']").prop("checked", true);
            button.closest('.form').hide();
            totalVisibleForms.val(parseInt(totalVisibleForms.val()) - 1)
            showBotonEliminar();
            showBotonAgregar();
        }

        /**
         * Genera los formularios a partir de formularios hermanos limpios
         */
        var addForms = function(){
            totalForms.val(parseInt(totalForms.val())+1);
            var regex = /\-{1}([0-9]{1,3})\-{1}/
            $("#"+elemBase.attr('id')+"> .form:not([style]):last").clone(true, true).insertAfter($("#"+elemBase.attr('id')+"> .form:last")) // clona el ultimo form
            $("#"+elemBase.attr('id')+"> .form:last [class='errorlist']").remove() // Elimina errores que genero el ultimo form si al enviar el formulario se genero alguno
            $("#"+elemBase.attr('id')+"> .form:last [id^='id_"+options.prefix+"']").each(function(){
                $(this).attr('id', $(this).attr('id').replace(regex, "-"+(parseInt(totalForms.val())-1)+"-"));
            }); // cambia el valor del id
            $("#"+elemBase.attr('id')+"> .form:last [for^='id_"+options.prefix+"']").each(function(){
                $(this).attr('for', $(this).attr('for').replace(regex, "-"+(parseInt(totalForms.val())-1)+"-"));
            }); // cambio el valor de los for
            $("#"+elemBase.attr('id')+"> .form:last [name^='"+options.prefix+"']").each(function(){
                $(this).attr('name', $(this).attr('name').replace(regex, "-"+(parseInt(totalForms.val())-1)+"-"));
            }); // cambia el valor de los name
            $("#"+elemBase.attr('id')+"> .form:last [id$='-DELETE'][type='button']").each(function(){
                $(this).attr('id', $(this).attr('id').replace(regex, "-"+(parseInt(totalForms.val())-1)+"-"));
            }); // cambia el valor de los name del boton ya que es especial al id del checkbox oculto
            $("#"+elemBase.attr('id')+"> .form:last [name^='"+options.prefix+"'][type!='button']").each(function(){
                if ($(this).attr('type')!='checkbox'){
                    $(this).val('');
                }
            }); // Formatear valores ingresados del elemento a clonar
            totalVisibleForms.val(parseInt(totalVisibleForms.val()) + 1)
            showBotonEliminar();
            showBotonAgregar();
        }

        /**
         * Oculta los formularios eliminados al inicio que ya fueron enviados pero no se genero corretamente 
         */
        var hiddenInicioForms = function(){
            $("#"+elemBase.attr('id')+" input[type='checkbox'][checked][id$='-DELETE']").closest('.form').hide()
        }

        addBotonAgregar();
        showBotonAgregar();
        $("#buttonAdd"+options.prefix).on('click', function(){
            addForms();
        })
        addBotonEliminar();
        showBotonEliminar();
        $("#"+elemBase.attr('id')+" > .form input[id$='-DELETE'][type='button']").each(function(){
            $(this).click(function(){deleteForms($(this))})
        })
        hiddenInicioForms();
        
    }

    $.fn.mensaje.defaults = {
        prefix: 'form',
        nameButton: 'Agregar',
        nameButtonDelete: 'Eliminar'
    }
})(jQuery);