/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

App.WidgetWizardStep2View = Em.View.extend({

  templateName: require('templates/main/service/widgets/create/step2'),

  /**
   * calculate template by widget type
   */
  templateType: function () {
    switch (this.get('controller.content.widgetType')) {
      case 'GAUGE':
      case 'NUMBER':
        return {
          isNumber: true
        };
      case 'TEMPLATE':
        return {
          isTemplate: true
        };
      case 'GRAPH':
        return {
          isGraph: true
        }
    }
  }.property('controller.content.widgetType'),

  didInsertElement: function () {
    var controller = this.get('controller');
    controller.initWidgetData();
    controller.renderProperties();
    controller.updateExpressions();
  }
});


App.WidgetPropertyTextFieldView = Em.TextField.extend({
  valueBinding: 'property.value',
  classNameBindings: ['property.classNames', 'parentView.basicClass']
});

App.WidgetPropertyThresholdView = Em.View.extend({
  templateName: require('templates/main/service/widgets/create/widget_property_threshold'),
  classNameBindings: ['property.classNames', 'parentView.basicClass']
});

App.WidgetPropertySelectView = Em.Select.extend({
  selectionBinding: 'property.value',
  contentBinding: 'property.options',
  classNameBindings: ['property.classNames', 'parentView.basicClass']
});



